from __future__ import annotations

import inspect
import functools

from typing import Optional
from typing import Any
from typing import Callable

from _elements.converters import Converter


class Parameter:
	__parameters = {}

	def __init__(self, func, default: Optional[dict], name: Optional[str] = None, converter: Optional[Converter] = None):
		functools.update_wrapper(self, func)
		self.__name = name or func.__name__

		self.__function = func
		self.__default = default
		self.__converter: Converter = converter

		Parameter.__parameters.update({name: self})

	@staticmethod
	def set(name: str, default: Optional[Any] = None) -> Callable[[{__name__}], Parameter]:
		def _param(function) -> Parameter:
			param: Parameter = Parameter(function, name=name, default=default)
			return param
		return _param

	@staticmethod
	def converter(name: str) -> Callable:
		def _conv(function: Parameter):
			instance: Parameter = function
			assert isinstance(function, Parameter)
			instance.__converter = Converter.get(name)

			@functools.wraps(function)
			def wrapper(*args, **kwargs):
				return function(*args, **kwargs)
			return wrapper
		return _conv

	def __call__(self, *args, **kwargs):
		from _query import Query  # TODO: Fix circular import error, and make this better
		print(f"In __call__: self: {self}, args: {args}, kwargs: {kwargs}")
		query: Query = args[0] if isinstance(args[0], Query) else None
		converted = self.__converter(*args, **kwargs) or None
		value = self.__function(*args, **kwargs)
		if "self" in inspect.signature(self.__function).parameters:
			args = tuple(list(args)[1:])
		if query:
			query.parameters.update(**converted or kwargs)
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
