import functools

from typing import Callable
from typing import TypeVar

TConverter = TypeVar("TConverter", bound="Converter")


class Converter:
	__converters = {}

	def __init__(self, func: Callable[[tuple, dict], dict], name):
		functools.update_wrapper(self, func)
		self.name = name
		self.func = func

		Converter.__converters.update({name: self})

	@staticmethod
	def set(name: str) -> Callable[[Callable[[tuple, dict], dict]], TConverter]:
		def _conv(function: Callable[[tuple, dict], dict]) -> TConverter:
			conv: Converter = Converter(function, name)
			return conv
		return _conv

	def __call__(self, *args, **kwargs) -> dict:
		converted = self.func(*args, **kwargs)
		return converted

	@staticmethod
	def get(name: str) -> TConverter:
		return Converter.__converters[name]


@Converter.set("select")
def select_converter(*args, **kwargs) -> dict:
	converted = {"columns": {}}
	for column in args:
		if not isinstance(column, str):
			continue
		if " as " in column:
			column = column.split()
			converted["columns"].update({column[0]: column[-1]})
		else:
			converted["columns"].update({column: column})
	return converted


@Converter.set("distinct")
def distinct_converter(*args, **kwargs):
	return args, kwargs
