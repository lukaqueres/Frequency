import inspect
import functools

import dataclasses
from dataclasses import dataclass

from typing import Optional
from typing import Any
from typing import TypeVar
from typing import Callable

TConverter = TypeVar("TConverter", bound="Converter")


@dataclass
class Converted:
	args: tuple = dataclasses.field(default_factory=tuple)
	kwargs: dict = dataclasses.field(default_factory=dict)


class Converter:
	__converters = {}

	def __init__(self, func, name):
		functools.update_wrapper(self, func)
		self.name = name
		self.func = func

		Converter.__converters.update({name: self})

	@staticmethod
	def set(name: str) -> Callable:
		def _conv(function) -> TConverter:
			conv = Converter(function, name)
			return conv
		return _conv

	def __call__(self, *args, **kwargs) -> Converted:
		converted_args, converted_kwargs = self.func(*args, **kwargs)
		return Converted(converted_args, converted_kwargs)

	@staticmethod
	def get(name: str) -> TConverter:
		return Converter.__converters[name]

	@staticmethod
	def use(name: str):
		def _use(func):
			@functools.wraps(func)
			def wrapper(*args, **kwargs):
				conv = Converter.__converters[name]
				args = list(args)
				args.append(conv(*args, **kwargs))
				args = tuple(args)
				value = func(*args, **kwargs)
				return value
			return wrapper
		return _use


@dataclass
class Cache:
	default: bool
	cache: dict[Any: Any] = dataclasses.field(default_factory=dict)
	called: dict[Any: Any] = dataclasses.field(default_factory=dict)

	def update(self, **kwargs):
		for attribute, value in kwargs.items():
			self.cache.update({attribute: value})
		self.default = False

	def get(self, key: str) -> Any:
		return self.cache[key]


class Parameter:
	__parameters = {}

	def __init__(self, func, default: Optional[dict], name: Optional[str] = None, converter: Optional[Converter] = None):
		functools.update_wrapper(self, func)
		self.__name = name or func.__name__

		self.__function = func
		self.__default = default
		self.__converter = converter
		self.__cache = Cache(default=True, cache=self.__default)

		Parameter.__parameters.update({name: self})

	@staticmethod
	def reset():
		for parameter in Parameter.__parameters:
			parameter.reload()

	def reload(self):
		self.__cache = Cache(default=True, cache=self.__default)

	@staticmethod
	def set(name: str, default: Optional[Any] = None):
		def _param(function):
			param = Parameter(function,name=name, default=default)
			return param
		return _param

	@staticmethod
	def converter(name: str):
		def _conv(function):
			instance = function if isinstance(function, Parameter) else function.__wraps__
			instance.__converter = Converter.get(name)

			@functools.wraps(function)
			def wrapper(*args, **kwargs):
				return function(*args, **kwargs)
			return wrapper
		return _conv

	def __call__(self, *args, **kwargs):
		print(f"In __call__: self: {self}, args: {args}, kwargs: {kwargs}")
		converted = self.__converter(*args, **kwargs) or None
		value = self.__function(*args, **kwargs)
		if "self" in inspect.signature(self.__function).parameters:
			args = tuple(list(args)[1:])
		if converted:
			self.__cache.update(args=converted.args)
			self.__cache.update(**converted.kwargs)
		else:
			self.__cache.update(args=args)
			self.__cache.update(**kwargs)
		print(f"Value: {value}")
		return value

	@staticmethod
	def get(parameter, attribute) -> Any:
		return getattr(parameter.__wrapped__.__wrapped__, attribute)

	@staticmethod
	def method(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)

		return wrapper

	@property
	def cache(self):
		return self.__cache


class SubQuery:
	def __init__(self, name):
		self.name = name

		self.__parameters = []
		self.__finishers = []

		self.parameter = Parameter
