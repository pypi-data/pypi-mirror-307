from tqdm import tqdm
from copy import deepcopy
import numpy as np
from typing import List, Tuple, Union
import torch
from torch import optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from torch.optim.lr_scheduler import LRScheduler, CosineAnnealingLR
from sklearn.model_selection import train_test_split
from nlpx import log_utils


def cal_count(y):
	shape = y.shape
	return shape[0] if len(shape) == 1 else shape[0] * shape[1]


def cal_correct(logits: torch.Tensor, y: torch.Tensor):
	if len(logits.size()) > 1:
		return (logits.argmax(-1) == y).sum()
	else:
		return (logits > 0.5).sum()


def evaluate(model, val_loader, device):
	total, steps = 0, 0
	total_loss, correct = [torch.Tensor([0.0]) for _ in range(2)]
	model.eval()
	with torch.no_grad():
		if hasattr(model, 'fit'):
			for batch in val_loader:
				batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
				y = batch[-1]
				loss, logits = model.fit(*batch)
				total_loss += loss
				total += cal_count(y)
				correct += cal_correct(logits, y)
				steps += 1
		else:
			for batch in val_loader:
				batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
				y = batch[-1]
				loss, logits = model(*batch)
				total_loss += loss
				total += cal_count(y)
				correct += cal_correct(logits, y)
				steps += 1
	return (total_loss.item() / steps), (correct.item() / total)


def do_train(model, batch, optimizer, device):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	loss, logits = model(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss


def do_fit(model, batch, optimizer, device):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	loss, logits = model.fit(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss


def do_train_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	loss, logits = model(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss


def do_fit_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	loss, logits = model.fit(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss


def do_train_acc(model, batch, optimizer, device):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	y = batch[-1]
	loss, logits = model(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_fit_acc(model, batch, optimizer, device):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	y = batch[-1]
	loss, logits = model.fit(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_train_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	y = batch[-1]
	loss, logits = model(*batch)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	scheduler.step()
	return loss, cal_count(y), cal_correct(logits, y)


def do_fit_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
	batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
	y = batch[-1]
	loss, logits = model.fit(*batch)
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


def train_epoch_progress(model, train_loader, optimizer, device, epoch, max_iter):
	steps = 0
	total_loss = torch.Tensor([0.0])
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{max_iter}]", total=len(train_loader), colour="green")
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


def train_epoch_scheduler_progress(model, train_loader, optimizer, device, scheduler, epoch, max_iter):
	steps = 0
	total_loss = torch.Tensor([0.0])
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{max_iter}]", total=len(train_loader), colour="green")
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


def train_epoch(model, train_loader, optimizer, device, scheduler, epoch, max_iter, show_progress):
	if show_progress:
		if scheduler is None:
			return train_epoch_progress(model, train_loader, optimizer, device, epoch, max_iter)
		return train_epoch_scheduler_progress(model, train_loader, optimizer, device, scheduler, epoch, max_iter)
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


def train_epoch_progress_acc(model, train_loader, optimizer, device, epoch, max_iter):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{max_iter}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, count, correct = do_fit_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}", train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, count, correct = do_train_acc(model, batch, optimizer, device)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}", train_loss=f"{total_loss.item() / steps:.4f}",
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


def train_epoch_scheduler_progress_acc(model, train_loader, optimizer, device, scheduler, epoch, max_iter):
	total, steps = 0, 0
	total_loss, total_correct = [torch.Tensor([0.0]) for _ in range(2)]
	loop = tqdm(train_loader, desc=f"[Epoch-{epoch}/{max_iter}]", total=len(train_loader), colour="green")
	if hasattr(model, 'fit'):
		for batch in loop:
			loss, count, correct = do_fit_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}", train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	else:
		for batch in loop:
			loss, count, correct = do_train_scheduler_acc(model, batch, optimizer, device, scheduler)
			total_loss += loss
			total += count
			total_correct += correct
			steps += 1
			loop.set_postfix(train_acc=f"{total_correct.item() / total:.4f}", train_loss=f"{total_loss.item() / steps:.4f}",
			                 lr=f'{optimizer.param_groups[0]["lr"]:.6f}')
	loop.close()
	
	return total_correct.item() / total, total_loss.item() / steps


def train_epoch_acc(model, train_loader, optimizer, device, scheduler, epoch, max_iter, show_progress):
	if show_progress:
		if scheduler is None:
			return train_epoch_progress_acc(model, train_loader, optimizer, device, epoch, max_iter)
		return train_epoch_scheduler_progress_acc(model, train_loader, optimizer, device, scheduler, epoch, max_iter)
	else:
		if scheduler is None:
			return train_epoch_base_acc(model, train_loader, optimizer, device)
		return train_epoch_scheduler_acc(model, train_loader, optimizer, device, scheduler)


class Trainer:
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "", persistent_workers: bool = False,
	             early_stopping_rounds: int = 2,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device
	             ):
		self.max_iter = max_iter
		self.optimizer = optimizer
		self.scheduler = scheduler
		self.learning_rate = learning_rate
		self.T_max = T_max
		self.batch_size = batch_size
		self.num_workers = num_workers
		self.pin_memory = pin_memory
		self.pin_memory_device = pin_memory_device
		self.persistent_workers = persistent_workers
		self.early_stopping_rounds = early_stopping_rounds
		self.print_per_rounds = print_per_rounds
		self.checkpoint_per_rounds = checkpoint_per_rounds
		self.checkpoint_name = checkpoint_name
		self.device = device or torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
	
	def train(self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		cnt = 0
		min_loss = float('inf')
		best_model = None
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		model.train()
		for epoch in range(1, self.max_iter + 1):
			avg_loss = train_epoch(model, train_loader, optimizer, self.device, scheduler, epoch, self.max_iter,
			                       show_progress)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss)
			self.try_checkpoint(model, epoch)
			
			if min_loss - avg_loss > eps:
				cnt = 0
				best_model = deepcopy(model)
				min_loss = avg_loss
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(3, self.early_stopping_rounds) and cnt >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.max_iter}")
				break
			
			cnt += 1
		
		return best_model
	
	def get_optimizer_scheduler(self, model):
		scheduler = None
		if self.scheduler is not None:
			scheduler = self.scheduler
			optimizer = scheduler.optimizer
		elif self.optimizer is None:
			optimizer = optim.AdamW(model.parameters(), lr=self.learning_rate)
		elif isinstance(self.optimizer, type):
			optimizer = self.optimizer(model.parameters(), lr=self.learning_rate)
		else:
			optimizer = self.optimizer
		
		if scheduler is None and self.T_max and self.T_max > 0:
			scheduler = CosineAnnealingLR(optimizer, T_max=self.T_max)
		
		return optimizer, scheduler
	
	def try_checkpoint(self, model, epoch):
		if self.checkpoint_per_rounds <= 0:
			return
		
		if self.checkpoint_per_rounds == 1 or epoch % self.checkpoint_per_rounds == 0:
			torch.save(model, self.checkpoint_name)
			
	def try_print(self, do_print, show_progress, epoch, lr, loss, **kwargs):
		if self.print_per_rounds == 1 or epoch % self.print_per_rounds == 0:
			do_print(show_progress, epoch, lr, loss, **kwargs)
			
	def print(self, show_progress, epoch, lr, loss):
		if show_progress:
			log_utils.info(f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, loss: {loss:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, loss: {loss:.4f}')


class SimpleTrainer(Trainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
		
		return super().train(model, TensorDataset(X, y), collate_fn, show_progress, eps=eps)


class ClassTrainer(Trainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		best_model = None
		min_loss = float('inf')
		cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		model.train()
		for epoch in range(1, self.max_iter + 1):
			acc, avg_loss = train_epoch_acc(model, train_loader, optimizer, self.device, scheduler, epoch,
			                                self.max_iter, show_progress)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss, acc=acc)
			self.try_checkpoint(model, epoch)
			
			if acc > best_acc or (acc == best_acc and min_loss - avg_loss > eps):
				cnt, cnt2 = 0, 0
				best_acc, best_model = acc, deepcopy(model)
				last_acc, min_loss = acc, min(min_loss, avg_loss)
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.max_iter}")
				break
			
			if abs(last_acc - acc) < eps:  # val_acc不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_acc = acc
			best_acc = max(best_acc, acc)
			min_loss = min(min_loss, avg_loss)
		
		return best_model
	
	def print(self, show_progress, epoch, lr, loss, acc):
		if show_progress:
			log_utils.info(f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}')


class SimpleClassTrainer(ClassTrainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
		
		return super().train(model, TensorDataset(X, y), collate_fn, show_progress, eps=eps)


class EvalClassTrainer(Trainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0, pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False, early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
		self.eval_batch_size = eval_batch_size
		self.num_eval_workers = num_eval_workers
	
	def train(self, model, train_set: Dataset, val_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		val_loader = DataLoader(dataset=val_set, batch_size=self.eval_batch_size,
		                        num_workers=self.num_eval_workers, collate_fn=collate_fn)
		best_model = None
		min_loss = float('inf')
		cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		for epoch in range(1, self.max_iter + 1):
			model.train()
			acc, avg_loss = train_epoch_acc(model, train_loader, optimizer, self.device, scheduler, epoch,
			                                self.max_iter, show_progress)
			
			val_loss, val_acc = evaluate(model, val_loader, self.device)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss,
			           acc=acc, val_loss=val_loss, val_acc=val_acc)
			self.try_checkpoint(model, epoch)
			
			if val_acc > best_acc or (val_acc == best_acc and min_loss - val_loss > eps):
				cnt, cnt2 = 0, 0
				best_acc, best_model = val_acc, deepcopy(model)
				last_acc, min_loss = val_acc, min(min_loss, val_loss)
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.max_iter}")
				break
			
			if abs(last_acc - val_acc) < eps:  # val_acc不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_acc = val_acc
			best_acc = max(best_acc, val_acc)
			min_loss = min(min_loss, val_loss)
		
		return best_model
	
	def print(self, show_progress, epoch, lr, loss, acc, val_loss, val_acc):
		if show_progress:
			log_utils.info(
				f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, '
				f'val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}\n')
		else:
			log_utils.info(
				f'Epoch-{epoch}/{self.max_iter}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, '
				f'val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}')


class EvalSimpleClassTrainer(EvalClassTrainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):

		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, eval_batch_size, num_workers,
		                 num_eval_workers, pin_memory, pin_memory_device, persistent_workers, early_stopping_rounds,
		                 print_per_rounds, checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, val_data: Tuple, collate_fn=None, show_progress=False, eps=1e-5):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
		X_val, y_val = val_data[0], val_data[1]
		if isinstance(X_val, (List, np.ndarray)):
			X_val = torch.tensor(X_val, dtype=torch.float)
		if isinstance(y_val, (List, np.ndarray)):
			y_val = torch.tensor(y_val, dtype=torch.long)
		
		return super().train(model, TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn, show_progress, eps)


class SplitClassTrainer(EvalSimpleClassTrainer):
	
	def __init__(self, max_iter=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(max_iter, optimizer, scheduler, learning_rate, T_max, batch_size, eval_batch_size, num_workers,
		                 num_eval_workers, pin_memory, pin_memory_device, persistent_workers, early_stopping_rounds,
		                 print_per_rounds, checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, val_size=0.2, random_state=None, collate_fn=None, show_progress=False, eps=1e-5):
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=val_size, random_state=random_state)
		return super().train(model, X_train, y_train, (X_test, y_test), collate_fn, show_progress, eps)
