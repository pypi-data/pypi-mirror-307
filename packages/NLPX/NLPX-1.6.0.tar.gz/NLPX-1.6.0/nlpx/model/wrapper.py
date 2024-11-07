import numpy as np
import pandas as pd
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader, Dataset

from nlpx.llm import TokenizeVec
from nlpx.dataset import TokenDataset, PaddingTokenCollator
from nlpx.text_token import BaseTokenizer, PaddingTokenizer, SimpleTokenizer, Tokenizer, TokenEmbedding
from nlpx.training import Trainer, SimpleTrainer, ClassTrainer, SimpleClassTrainer, SplitClassTrainer, evaluate, \
	EvalClassTrainer, EvalSimpleClassTrainer


class ModelWrapper:
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import ModelWrapper
	>>> model_wrapper = ModelWrapper(model)
	>>> model_wrapper.train(train_set, val_set, collate_fn)
	>>> model_wrapper.logits(X_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path], device: torch.device = None):
		if isinstance(model_or_path, nn.Module):
			self.model, self.best_model = model_or_path, model_or_path
		elif isinstance(model_or_path, (str, Path)):
			self.model = torch.load(model_or_path, map_location=device)
			self.best_model = self.model
		self.device = device or torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
	
	def train(self, train_set: Dataset, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		trainer = Trainer(max_iter, optimizer, scheduler, learning_rate, T_max,
		                  batch_size,
		                  num_workers,
		                  pin_memory, pin_memory_device,
		                  persistent_workers,
		                  early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                  print_per_rounds,
		                  checkpoint_per_rounds,
		                  checkpoint_name,
		                  self.device)
		self.best_model = trainer.train(self.model, train_set, collate_fn, show_progress, eps)
	
	def logits(self, X: torch.Tensor):
		self.best_model.eval()
		with torch.no_grad():
			logits = self.best_model(X)
		return logits
	
	def save(self, best_model_path: Union[str, Path] = './best_model.pt', 
	         last_model_path: Union[str, Path] = './last_model.pt', save_mode: str = 'both'):
		"""
		:param best_model_path: 
		:param last_model_path: 
		:param save_mode: "both" or "best" or "last"
		:return: 
		"""
		assert save_mode in ('both', 'best', 'last')
		if save_mode == 'both':
			torch.save(self.model, last_model_path)
			torch.save(self.best_model, best_model_path)
		elif save_mode == 'best':
			torch.save(self.best_model, best_model_path)
		elif save_mode == 'last':
			torch.save(self.model, last_model_path)
	
	def load(self, model_path: Union[str, Path] = './best_model.pt'):
		self.model = torch.load(model_path, map_location=self.device)
		self.best_model = self.model


class SimpleModelWrapper(ModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SimpleModelWrapper
	>>> model_wrapper = SimpleModelWrapper(model)
	>>> model_wrapper.train(X, y, collate_fn)
	>>> model_wrapper.logits(X_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path],
	             device: torch.device = None):
		super().__init__(model_or_path, device)
	
	def train(self, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		trainer = SimpleTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
		                        batch_size,
		                        num_workers,
		                        pin_memory, pin_memory_device,
		                        persistent_workers,
		                        early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                        print_per_rounds,
		                        checkpoint_per_rounds,
		                        checkpoint_name,
		                        self.device)
		self.best_model = trainer.train(self.model, X, y, collate_fn, show_progress, eps)


class ClassModelWrapper(ModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import ClassModelWrapper
	>>> model_wrapper = ClassModelWrapper(model, classes=classes)
	>>> model_wrapper.train(train_set, val_set, collate_fn)
	>>> model_wrapper.predict(X_test)
	>>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path], classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, device)
		self.classes = classes
	
	def train(self, train_set: Dataset, val_set: Dataset = None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		if val_set:
			trainer = EvalClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                           batch_size, eval_batch_size,
			                           num_workers, num_eval_workers,
			                           pin_memory, pin_memory_device,
			                           persistent_workers,
			                           early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
			                           print_per_rounds,
			                           checkpoint_per_rounds,
			                           checkpoint_name,
			                           self.device)
			self.best_model = trainer.train(self.model, train_set, val_set, collate_fn, show_progress, eps)
		else:
			trainer = ClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                       batch_size, num_workers,
			                       pin_memory, pin_memory_device,
			                       persistent_workers,
			                       early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
			                       print_per_rounds,
			                       checkpoint_per_rounds,
			                       checkpoint_name,
			                       self.device)
			self.best_model = trainer.train(self.model, train_set, collate_fn, show_progress, eps)
	
	def predict(self, X: torch.Tensor):
		logits = self.logits(X)
		return logits.argmax(-1)
	
	def predict_classes(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(X)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, X: torch.Tensor):
		logits = self.logits(X)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(X)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def evaluate(self, val_set: Dataset, batch_size=64, num_workers=0, collate_fn=None):
		val_loader = DataLoader(dataset=val_set, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)
		_, acc = evaluate(self.best_model, val_loader, self.device)
		return acc


class SimpleClassModelWrapper(ClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SimpleClassModelWrapper
	>>> model_wrapper = SimpleClassModelWrapper(model, classes=classes)
	>>> model_wrapper.train(X, y val_data, collate_fn)
	>>> model_wrapper.predict(X_test)
	>>> model_wrapper.evaluate(X_test, y_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path], classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, classes, device)
	
	def train(self, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[Union[torch.Tensor, np.ndarray, List], Union[torch.LongTensor, np.ndarray, List]] = None,
	          collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		if val_data:
			trainer = EvalSimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                                 batch_size, eval_batch_size,
			                                 num_workers, num_eval_workers,
			                                 pin_memory, pin_memory_device,
			                                 persistent_workers,
			                                 early_stopping_rounds,
			                                 print_per_rounds,
			                                 checkpoint_per_rounds,
			                                 checkpoint_name,
			                                 self.device)
			self.best_model = trainer.train(self.model, X, y, val_data, collate_fn, show_progress, eps)
		else:
			trainer = SimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                             batch_size, num_workers,
			                             pin_memory, pin_memory_device,
			                             persistent_workers,
			                             early_stopping_rounds,
			                             print_per_rounds,
			                             checkpoint_per_rounds,
			                             checkpoint_name,
			                             self.device)
			self.best_model = trainer.train(self.model, X, y, collate_fn, show_progress, eps)
	
	def evaluate(self, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	             batch_size=64, num_workers=0, collate_fn=None):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
			
		data_set = TokenDataset(X, y)
		return super().evaluate(data_set, batch_size, num_workers, collate_fn)


class TextModelWrapper(SimpleClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import TextModelWrapper
	>>> model_wrapper = TextModelWrapper(model, tokenize_vec, classes=classes)
	>>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path], 
	             tokenize_vec: Union[BaseTokenizer, TokenizeVec, TokenEmbedding],
	             classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, classes, device)
		self.tokenize_vec = tokenize_vec
	
	def train(self, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[
		          Union[Collection[str], np.ndarray, pd.Series], Union[torch.LongTensor, np.ndarray, List]] = None,
	          max_length: int = None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          n_jobs=-1, show_progress=False, eps=1e-5):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		if val_data:
			val_data = (self.get_vec(val_data[0], max_length=max_length, n_jobs=-1), val_data[1])
		super().train(X, y, val_data, collate_fn, max_iter, optimizer, scheduler, learning_rate, T_max,
		              batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory, pin_memory_device,
		              persistent_workers, early_stopping_rounds, print_per_rounds, checkpoint_per_rounds,
		              checkpoint_name, show_progress, eps)
	
	def predict(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		return logits.argmax(-1)
	
	def predict_classes(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length, n_jobs=n_jobs)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length, n_jobs)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, Collection[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=64, num_workers=0,
	             max_length: int = None, collate_fn=None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		return super().evaluate(X, y, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)
	
	def get_vec(self, texts: Union[str, Collection[str], np.ndarray, pd.Series], max_length: int, n_jobs: int):
		if isinstance(texts, str):
			texts = [texts]
		
		if isinstance(self.tokenize_vec, TokenizeVec):
			return self.tokenize_vec.parallel_encode_plus(texts, max_length=max_length, padding='max_length',
			                                              truncation=True, add_special_tokens=True,
			                                              return_token_type_ids=True, return_attention_mask=True,
			                                              return_tensors='pt', n_jobs=n_jobs)
		
		elif isinstance(self.tokenize_vec, (PaddingTokenizer, SimpleTokenizer, Tokenizer)):
			return torch.LongTensor(self.tokenize_vec.batch_encode(texts, max_length))
		
		elif isinstance(self.tokenize_vec, TokenEmbedding):
			return self.tokenize_vec(texts, max_length)
		
		raise ValueError("Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding.")


class SplitTextModelWrapper(TextModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SplitTextModelWrapper
	>>> model_wrapper = SplitTextModelWrapper(model, tokenize_vec, classes=classes)
	>>> model_wrapper.train(texts, y, collate_fn)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path],
	             tokenize_vec: Union[BaseTokenizer, TokenizeVec, TokenEmbedding],
	             classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, tokenize_vec, classes, device)
	
	def train(self, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval=True, val_size=0.2, random_state=None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          n_jobs=-1, show_progress=False, eps=1e-5):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		if eval:
			trainer = SplitClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                            batch_size, eval_batch_size,
			                            num_workers, num_eval_workers,
			                            pin_memory, pin_memory_device,
			                            persistent_workers,
			                            early_stopping_rounds,
			                            print_per_rounds,
			                            checkpoint_per_rounds,
			                            checkpoint_name,
			                            self.device)
			self.best_model = trainer.train(self.model, X, y, val_size, random_state, collate_fn, show_progress, eps)
		else:
			trainer = SimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                             batch_size, num_workers,
			                             pin_memory, pin_memory_device,
			                             persistent_workers,
			                             early_stopping_rounds,
			                             print_per_rounds,
			                             checkpoint_per_rounds,
			                             checkpoint_name,
			                             self.device)
			self.best_model = trainer.train(self.model, X, y, collate_fn, show_progress, eps)


class PaddingTextModelWrapper(ClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import PaddingTextModelWrapper
	>>> model_wrapper = PaddingTextModelWrapper(model, tokenizer, classes=classes)
	>>> model_wrapper.train(train_texts, y_train val_data)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	def __init__(self, model_or_path: Union[nn.Module, str, Path],
	             tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
	             classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, classes, device)
		self.tokenizer = tokenizer
	
	def train(self, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[Union[Collection[str], np.ndarray, pd.Series], Union[torch.LongTensor, np.ndarray, List]] = None,
	          max_length: int = None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		X = self.tokenizer.batch_encode(texts, padding=False)
		train_set = TokenDataset(X, y)
		val_set = None
		if val_data:
			X_val = self.tokenizer.batch_encode(val_data[0], padding=False)
			val_set = TokenDataset(X_val, val_data[1])
		
		super().train(self.model, train_set, val_set, collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
		              max_iter=max_iter, optimizer=optimizer, scheduler=scheduler, learning_rate=learning_rate,
		              T_max=T_max, batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory,
		              pin_memory_device=pin_memory_device, persistent_workers=persistent_workers,
		              early_stopping_rounds=early_stopping_rounds, print_per_rounds=print_per_rounds,
		              checkpoint_per_rounds=checkpoint_per_rounds, checkpoint_name=checkpoint_name,
		              show_progress=show_progress, eps=eps)
	
	def predict(self, texts: Collection[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		return logits.argmax(-1)
	
	def predict_classes(self, texts: Collection[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: Collection[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: Collection[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: Collection[str], max_length: int = None):
		X = self.tokenizer.batch_encode(texts, max_length)
		X = torch.tensor(X, dtype=torch.long)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, Collection[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=64, num_workers=0,
	             max_length: int = None):
		X = self.tokenizer.batch_encode(texts, padding=False)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		val_set = TokenDataset(X, y)
		return super().evaluate(val_set, batch_size=batch_size, num_workers=num_workers,
		                        collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length))


class SplitPaddingTextModelWrapper(PaddingTextModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SplitPaddingTextModelWrapper
	>>> model_wrapper = SplitPaddingTextModelWrapper(tokenizer, classes=classes)
	>>> model_wrapper.train(model, texts, y)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path],
	             tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
	             classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, tokenizer, classes, device)
	
	def train(self, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval=True, val_size=0.2, random_state=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5):
		val_data = None
		if eval:
			X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=val_size, random_state=random_state)
			val_data = (X_test, y_test)
		else:
			X_train, y_train = texts, y
		
		super().train(X_train, y_train, val_data, max_length, max_iter, optimizer, scheduler, learning_rate,
		              T_max, batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory, pin_memory_device,
		              persistent_workers, early_stopping_rounds, print_per_rounds, checkpoint_per_rounds,
		              checkpoint_name, show_progress, eps)
