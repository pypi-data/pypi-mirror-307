from copy import deepcopy
import numpy as np
from typing import List, Tuple, Union
import torch
from torch import optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from torch.optim.lr_scheduler import LRScheduler, CosineAnnealingLR

from nlpx import log_utils
from .utils import train_epoch, train_epoch_acc, evaluate, acc_evaluate, r2_evaluate, train_epoch_r2, convert_data,\
	convert_data_acc, convert_data_r2


class Trainer:
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "", persistent_workers: bool = False,
	             early_stopping_rounds: int = 2,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device
	             ):
		self.epochs = epochs
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
		for epoch in range(1, self.epochs + 1):
			avg_loss = train_epoch(model, train_loader, optimizer, self.device, scheduler, epoch, self.epochs,
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
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
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
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}')


class SimpleTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data(X, y)
		return super().train(model, TensorDataset(X, y), collate_fn, show_progress, eps=eps)


class EvalTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0, pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False, early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	             device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
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
		cnt = 0
		best_model = None
		min_loss = float('inf')
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		for epoch in range(1, self.epochs + 1):
			model.train()
			avg_loss = train_epoch(model, train_loader, optimizer, self.device, scheduler, epoch, self.epochs,
			                       show_progress)
			val_loss = evaluate(model, val_loader, self.device)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss, val_loss=val_loss)
			self.try_checkpoint(model, epoch)
			
			if min_loss - val_loss > eps:
				cnt = 0
				best_model = deepcopy(model)
				min_loss = val_loss
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(3, self.early_stopping_rounds) and cnt >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
				break
			
			cnt += 1
		
		return best_model
	
	def print(self, show_progress, epoch, lr, loss, val_loss):
		if show_progress:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, val_loss: {val_loss:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, val_loss: {val_loss:.4f}')


class SimpleEvalTrainer(EvalTrainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	             device=torch.device):
		
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, eval_batch_size, num_workers,
		                 num_eval_workers, pin_memory, pin_memory_device, persistent_workers, early_stopping_rounds,
		                 print_per_rounds, checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, val_data: Tuple, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data(X, y)
		X_val, y_val = convert_data(val_data[0], val_data[1])
		return super().train(model, TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn, show_progress, eps)
		

class ClassTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
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
		for epoch in range(1, self.epochs + 1):
			acc, avg_loss = train_epoch_acc(model, train_loader, optimizer, self.device, scheduler, epoch,
			                                self.epochs, show_progress)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss, acc=acc)
			self.try_checkpoint(model, epoch)
			
			if acc > best_acc or (acc == best_acc and min_loss - avg_loss > eps):
				cnt, cnt2 = 0, 0
				best_acc, best_model = acc, deepcopy(model)
				last_acc, min_loss = acc, min(min_loss, avg_loss)
				continue
			
			# x次epoch的val_acc不提升或x次epoch的val_acc不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
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
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}')


class SimpleClassTrainer(ClassTrainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data_acc(X, y)
		return super().train(model, TensorDataset(X, y), collate_fn, show_progress, eps=eps)


class EvalClassTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0, pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False, early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
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
		
		for epoch in range(1, self.epochs + 1):
			model.train()
			acc, avg_loss = train_epoch_acc(model, train_loader, optimizer, self.device, scheduler, epoch,
			                                self.epochs, show_progress)
			
			val_loss, val_acc = acc_evaluate(model, val_loader, self.device)
			
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
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
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
				f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, '
				f'val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}\n')
		else:
			log_utils.info(
				f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, '
				f'val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}')


class SimpleEvalClassTrainer(EvalClassTrainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):

		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, eval_batch_size, num_workers,
		                 num_eval_workers, pin_memory, pin_memory_device, persistent_workers, early_stopping_rounds,
		                 print_per_rounds, checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, val_data: Tuple, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data_acc(X, y)
		X_val, y_val = convert_data_acc(val_data[0], val_data[1])
		return super().train(model, TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn, show_progress, eps)
		

class RegressTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt', device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5):
		train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, pin_memory=self.pin_memory,
		                          pin_memory_device=self.pin_memory_device, persistent_workers=self.persistent_workers,
		                          num_workers=self.num_workers, shuffle=True, collate_fn=collate_fn)
		best_model = model
		min_loss = float('inf')
		cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		model.train()
		for epoch in range(1, self.epochs + 1):
			r2, avg_loss = train_epoch_r2(model, train_loader, optimizer, self.device, scheduler, epoch,
			                               self.epochs, show_progress)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss, r2=r2)
			self.try_checkpoint(model, epoch)
			
			if r2 > best_r2 or (r2 == best_r2 and min_loss - avg_loss > eps):
				cnt, cnt2 = 0, 0
				best_r2, best_model = r2, deepcopy(model)
				last_r2, min_loss = r2, min(min_loss, avg_loss)
				continue
			
			# x次epoch的val_r2不提升或x次epoch的val_r2不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
				break
			
			if abs(last_r2 - r2) < eps:  # val_r2不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_r2 = r2
			best_r2 = max(best_r2, r2)
			min_loss = min(min_loss, avg_loss)
		
		return best_model
	
	def print(self, show_progress, epoch, lr, loss, r2):
		if show_progress:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}\n')
		else:
			log_utils.info(f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}')


class SimpleRegressTrainer(RegressTrainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, num_workers=1,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	             device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
		                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds,
		                 checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data_r2(X, y)
		return super().train(model, TensorDataset(X, y), collate_fn, show_progress, eps=eps)


class EvalRegressTrainer(Trainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0, pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False, early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	             device=torch.device):
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, num_workers, pin_memory,
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
		best_model = model
		min_loss = float('inf')
		cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
		optimizer, scheduler = self.get_optimizer_scheduler(model)
		
		for epoch in range(1, self.epochs + 1):
			model.train()
			r2, avg_loss = train_epoch_r2(model, train_loader, optimizer, self.device, scheduler, epoch,
			                                self.epochs, show_progress)
			
			val_loss, val_r2 = r2_evaluate(model, val_loader, self.device)
			
			self.try_print(self.print, show_progress, epoch, optimizer.param_groups[0]["lr"], avg_loss,
			               r2=r2, val_loss=val_loss, val_r2=val_r2)
			self.try_checkpoint(model, epoch)
			
			if val_r2 > best_r2 or (val_r2 == best_r2 and min_loss - val_loss > eps):
				cnt, cnt2 = 0, 0
				best_r2, best_model = val_r2, deepcopy(model)
				last_r2, min_loss = val_r2, min(min_loss, val_loss)
				continue
			
			# x次epoch的val_r2不提升或x次epoch的val_r2不变化
			if epoch >= min(5, self.early_stopping_rounds) and max(cnt, cnt2) >= self.early_stopping_rounds:
				log_utils.info(f"Early stopping at Epoch-{epoch}/{self.epochs}")
				break
			
			if abs(last_r2 - val_r2) < eps:  # val_r2不在变化
				cnt2 += 1
			else:
				cnt2 = 0
			
			cnt += 1
			last_r2 = val_r2
			best_r2 = max(best_r2, val_r2)
			min_loss = min(min_loss, val_loss)
		
		return best_model
	
	def print(self, show_progress, epoch, lr, loss, r2, val_loss, val_r2):
		if show_progress:
			log_utils.info(
				f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}, '
				f'val_loss: {val_loss:.4f}, val_r2: {val_r2:.4f}\n')
		else:
			log_utils.info(
				f'Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}, '
				f'val_loss: {val_loss:.4f}, val_r2: {val_r2:.4f}')


class SimpleEvalRegressTrainer(EvalRegressTrainer):
	
	def __init__(self, epochs=100, optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	             learning_rate=0.001, T_max: int = 0, batch_size=32, eval_batch_size=64,
	             num_workers=0, num_eval_workers=0,
	             pin_memory: bool = False, pin_memory_device: str = "",
	             persistent_workers: bool = False,
	             early_stopping_rounds=10,  # 早停，等10轮决策，评价指标不在变化，停止
	             print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	             device=torch.device):
		
		super().__init__(epochs, optimizer, scheduler, learning_rate, T_max, batch_size, eval_batch_size, num_workers,
		                 num_eval_workers, pin_memory, pin_memory_device, persistent_workers, early_stopping_rounds,
		                 print_per_rounds, checkpoint_per_rounds, checkpoint_name, device)
	
	def train(self, model, X, y, val_data: Tuple, collate_fn=None, show_progress=False, eps=1e-5):
		X, y = convert_data_r2(X, y)
		X_val, y_val = convert_data_r2(val_data[0], val_data[1])
		return super().train(model, TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn, show_progress, eps)
