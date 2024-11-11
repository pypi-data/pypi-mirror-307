import inspect
from typing import Collection, List
import numpy as np
from tqdm import tqdm
from sklearn.metrics import r2_score
import torch
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler


def is_float(x):
	if isinstance(x, (Collection, np.ndarray)):
		return is_float(x[0])
	return isinstance(x, (float, np.float_, np.float16, np.float16, np.float32, np.float64, np.float128, np.single, np.double))


def convert_data(X, y):
	if isinstance(X, (List, np.ndarray)):
		X = torch.tensor(X, dtype=torch.float) if is_float(X[0][0]) else torch.tensor(X, dtype=torch.long)
	if isinstance(y, (List, np.ndarray)):
		y = torch.tensor(y, dtype=torch.float) if is_float(y[0]) else torch.tensor(y, dtype=torch.long)
	return X, y


def convert_data_acc(X, y):
	if isinstance(X, (List, np.ndarray)):
		X = torch.tensor(X, dtype=torch.float) if is_float(X[0][0]) else torch.tensor(X, dtype=torch.long)
	if isinstance(y, (List, np.ndarray)):
		y = torch.tensor(y, dtype=torch.long)
	return X, y


def convert_data_r2(X, y):
	if isinstance(X, (List, np.ndarray)):
		X = torch.tensor(X, dtype=torch.float) if is_float(X[0][0]) else torch.tensor(X, dtype=torch.long)
	if isinstance(y, (List, np.ndarray)):
		y = torch.tensor(y, dtype=torch.float)
	return X, y


def cal_count(y):
	shape = y.shape
	return shape[0] if len(shape) == 1 else shape[0] * shape[1]


def evaluate(model, val_loader, device):
	total, steps = 0, 0
	total_loss = torch.Tensor([0.0])
	model.eval()
	with torch.no_grad():
		if hasattr(model, 'fit'):
			for batch in val_loader:
				loss, logits = _fit(model, batch, device)
				total_loss += loss
				steps += 1
		else:
			for batch in val_loader:
				loss, logits = _train(model, batch, device)
				total_loss += loss
				steps += 1
	return total_loss.item() / steps


def r2_loss_logits(outputs, targets):
	if isinstance(outputs, tuple):
		loss, logits = outputs
	else:
		logits = outputs
		loss = F.mse_loss(outputs, targets.view(-1, 1))
	return loss, logits


def r2_evaluate(model, val_loader, device):
	total, steps = 0, 0
	total_loss = torch.Tensor([0.0])
	labels, preds = [], []
	model.eval()
	with torch.no_grad():
		if hasattr(model, 'fit'):
			for batch in val_loader:
				outputs, y = _fit_y(model, batch, device)
				loss, logits = r2_loss_logits(outputs, y)
				total_loss += loss
				steps += 1
				labels.extend(y.detach().numpy())
				preds.extend(logits.detach().numpy().flatten())
		else:
			for batch in val_loader:
				outputs, y = _train_y(model, batch, device)
				loss, logits = r2_loss_logits(outputs, y)
				total_loss += loss
				steps += 1
				labels.extend(y.detach().tolist())
				preds.extend(logits.detach().numpy().flatten().tolist())
	return total_loss.item() / steps, r2_score(np.array(labels), np.array(preds))


def cal_correct(logits: torch.Tensor, y: torch.Tensor):
	if len(logits.size()) > 1:
		return (logits.argmax(-1) == y).sum()
	else:
		return (logits > 0.5).sum()


def acc_loss_logits(outputs, targets):
	if isinstance(outputs, tuple):
		loss, logits = outputs
	else:
		logits = outputs
		shapes = len(logits.size())
		if shapes == 2:
			loss = F.cross_entropy(outputs, targets)
		elif shapes == 3:
			loss = F.cross_entropy(outputs.reshape(-1, outputs.size(2)), targets.view(-1))
		else:
			raise ValueError("logits shapes must be 2 or 3")
	return loss, logits


def acc_evaluate(model, val_loader, device):
	total, steps = 0, 0
	total_loss, correct = [torch.Tensor([0.0]) for _ in range(2)]
	model.eval()
	with torch.no_grad():
		if hasattr(model, 'fit'):
			for batch in val_loader:
				outputs, y = _fit_y(model, batch, device)
				loss, logits = acc_loss_logits(outputs, y)
				total_loss += loss
				total += cal_count(y)
				correct += cal_correct(logits, y)
				steps += 1
		else:
			for batch in val_loader:
				outputs, y = _train_y(model, batch, device)
				loss, logits = acc_loss_logits(outputs, y)
				total_loss += loss
				total += cal_count(y)
				correct += cal_correct(logits, y)
				steps += 1
	return (total_loss.item() / steps), (correct.item() / total)


def _train(model, batch, device):
	if isinstance(batch, dict):
		batch = {key: value.to(device) if torch.is_tensor(value) else value for key, value in batch.items()}
		return model(**batch)
	else:
		batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
		return model(*batch)


def _fit(model, batch, device):
	if isinstance(batch, dict):
		batch = {key: value.to(device) if torch.is_tensor(value) else value for key, value in batch.items()}
		return model.fit(**batch)
	else:
		batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
		return model.fit(*batch)
	

def do_train(model, batch, optimizer, device):
	loss, logits = _train(model, batch, device)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss


def do_fit(model, batch, optimizer, device):
	loss, logits = _fit(model, batch, device)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss


def do_train_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
	loss, logits = _train(model, batch, device)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss


def do_fit_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
	loss, logits = _fit(model, batch, device)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss


def _train_y(model, batch, device):
	same_params = len(batch) == len(inspect.signature(model.forward).parameters)  # 判断所传参数个数是否与方法一致
	if isinstance(batch, dict):
		batch = {key: value.to(device) if torch.is_tensor(value) else value for key, value in batch.items()}
		if same_params:
			y = batch['labels'] if 'labels' in batch else batch['targets']
		else:  # 参数个数不一致，要把 'labels' 或 'targets' 从参数里剔除
			y = batch.pop('labels') if 'labels' in batch else batch.pop('targets')
		return model(**batch), y
	else:
		batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
		if same_params:
			return model(*batch), batch[-1]
		# 参数个数不一致，去掉最后一个
		return model(*(batch[:-1])), batch[-1]


def _fit_y(model, batch, device):
	if isinstance(batch, dict):
		batch = {key: value.to(device) if torch.is_tensor(value) else value for key, value in batch.items()}
		return model.fit(**batch), batch['labels'] if 'labels' in batch else batch['targets']
	else:
		batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
		return model.fit(*batch), batch[-1]


def do_train_acc(model, batch, optimizer, device):
	outputs, y = _train_y(model, batch, device)
	loss, logits = acc_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_fit_acc(model, batch, optimizer, device):
	outputs, y = _fit_y(model, batch, device)
	loss, logits = acc_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_train_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
	outputs, y = _train_y(model, batch, device)
	loss, logits = acc_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_fit_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
	outputs, y = _fit_y(model, batch, device)
	loss, logits = acc_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss, cal_count(y), cal_correct(logits, y)


def train_epoch_base(model, train_loader, optimizer, device):
	steps = 0
	total_loss = torch.Tensor([0.0])
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss = do_fit(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
	else:
		for batch in train_loader:
			loss = do_train(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
	
	return total_loss.item() / steps


def train_epoch_progress(model, train_loader, optimizer, device, epoch, epochs):
	steps = 0
	total_loss = torch.Tensor([0.0])
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss = do_fit(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			loop.set_postfix(train_loss=f"{total_loss.item() / steps:.4f}", lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss = do_train(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			loop.set_postfix(train_loss=f"{total_loss.item() / steps:.4f}", lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	return total_loss.item() / steps


def train_epoch_scheduler(model, train_loader, optimizer, device, scheduler: LRScheduler):
	steps = 0
	total_loss = torch.Tensor([0.0])
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
	else:
		for batch in train_loader:
			loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
	return total_loss.item() / steps


def train_epoch_scheduler_progress(model, train_loader, optimizer, device, scheduler, epoch, epochs):
	steps = 0
	total_loss = torch.Tensor([0.0])
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			loop.set_postfix(train_loss=f"{total_loss.item() / steps:.4f}", lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			loop.set_postfix(train_loss=f"{total_loss.item() / steps:.4f}", lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	return total_loss.item() / steps


def train_epoch(model, train_loader, optimizer, device, scheduler, epoch, epochs, show_progress):
	if show_progress:
		if scheduler is None:
			return train_epoch_progress(model, train_loader, optimizer, device, epoch, epochs)
		return train_epoch_scheduler_progress(model, train_loader, optimizer, device, scheduler, epoch, epochs)
	else:
		if scheduler is None:
			return train_epoch_base(model, train_loader, optimizer, device)
		return train_epoch_scheduler(model, train_loader, optimizer, device, scheduler)


def train_epoch_base_acc(model, train_loader, optimizer, device):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss, count, correct = do_fit_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
	else:
		for batch in train_loader:
			loss, count, correct = do_train_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
	return total_correct.item() / total, total_loss.item() / steps


def train_epoch_progress_acc(model, train_loader, optimizer, device, epoch, epochs):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, count, correct = do_fit_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, count, correct = do_train_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	
	return total_correct.item() / total, total_loss.item() / steps


def train_epoch_scheduler_acc(model, train_loader, optimizer, device, scheduler: LRScheduler):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss, count, correct = do_fit_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
	else:
		for batch in train_loader:
			loss, count, correct = do_train_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
	return total_correct.item() / total, total_loss.item() / steps


def train_epoch_scheduler_progress_acc(model, train_loader, optimizer, device, scheduler, epoch, epochs):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, count, correct = do_fit_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, count, correct = do_train_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	
	return total_correct.item() / total, total_loss.item() / steps


def train_epoch_acc(model, train_loader, optimizer, device, scheduler, epoch, epochs, show_progress):
	if show_progress:
		if scheduler is None:
			return train_epoch_progress_acc(model, train_loader, optimizer, device, epoch, epochs)
		return train_epoch_scheduler_progress_acc(model, train_loader, optimizer, device, scheduler, epoch, epochs)
	else:
		if scheduler is None:
			return train_epoch_base_acc(model, train_loader, optimizer, device)
		return train_epoch_scheduler_acc(model, train_loader, optimizer, device, scheduler)

################################################################################


def train_epoch_r2(model, train_loader, optimizer, device, scheduler, epoch, epochs, show_progress):
	if show_progress:
		if scheduler is None:
			return train_epoch_progress_r2(model, train_loader, optimizer, device, epoch, epochs)
		return train_epoch_scheduler_progress_r2(model, train_loader, optimizer, device, scheduler, epoch, epochs)
	else:
		if scheduler is None:
			return train_epoch_base_r2(model, train_loader, optimizer, device)
		return train_epoch_scheduler_r2(model, train_loader, optimizer, device, scheduler)


def train_epoch_base_r2(model, train_loader, optimizer, device):
	steps = 0
	total_loss = torch.Tensor([0.0])
	labels, preds = [], []
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss, label, pred = do_fit_r2(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
	else:
		for batch in train_loader:
			loss, label, pred = do_train_r2(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
	return r2_score(np.array(labels), np.array(preds)), total_loss.item() / steps


def train_epoch_progress_r2(model, train_loader, optimizer, device, epoch, epochs):
	steps = 0
	total_loss = torch.Tensor([0.0])
	labels, preds = [], []
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, label, pred = do_fit_r2(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
			loop.set_postfix(train_r2=f"{r2_score(np.array(labels), np.array(preds)):.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, label, pred = do_train_r2(model, batch, optimizer, device)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
			loop.set_postfix(train_r2=f"{r2_score(np.array(labels), np.array(preds)):.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	
	return r2_score(np.array(labels), np.array(preds)), total_loss.item() / steps


def train_epoch_scheduler_r2(model, train_loader, optimizer, device, scheduler: LRScheduler):
	steps = 0
	total_loss = torch.Tensor([0.0])
	labels, preds = [], []
	if hasattr(model, 'fit'):
		for batch in train_loader:
			loss, label, pred = do_fit_scheduler_r2(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
	else:
		for batch in train_loader:
			loss, label, pred = do_train_scheduler_r2(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
	return r2_score(np.array(labels), np.array(preds)), total_loss.item() / steps


def train_epoch_scheduler_progress_r2(model, train_loader, optimizer, device, scheduler, epoch, epochs):
	steps = 0
	total_loss = torch.Tensor([0.0])
	labels, preds = [], []
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{epochs}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, label, pred = do_fit_scheduler_r2(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
			loop.set_postfix(train_r2=f"{r2_score(np.array(labels), np.array(preds)):.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, label, pred = do_train_scheduler_r2(model, batch, optimizer, device, scheduler)
			total_loss += loss
			steps += 1
			labels.extend(label)
			preds.extend(pred)
			loop.set_postfix(train_r2=f"{r2_score(np.array(labels), np.array(preds)):.4f}",
			                 train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	
	return r2_score(np.array(labels), np.array(preds)), total_loss.item() / steps


def do_train_r2(model, batch, optimizer, device):
	outputs, y = _train_y(model, batch, device)
	loss, logits = r2_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, y.detach().tolist(), logits.detach().numpy().flatten().tolist()


def do_fit_r2(model, batch, optimizer, device):
	outputs, y = _fit_y(model, batch, device)
	loss, logits = r2_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, y.detach().tolist(), logits.detach().numpy().flatten().tolist()


def do_train_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler):
	outputs, y = _train_y(model, batch, device)
	loss, logits = r2_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss, y.detach().tolist(), logits.detach().numpy().flatten().tolist()


def do_fit_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler):
	outputs, y = _fit_y(model, batch, device)
	loss, logits = r2_loss_logits(outputs, y)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss, y.detach().tolist(), logits.detach().numpy().flatten().tolist()
