import logging

from Errors import AttributeNotFoundError
from typing import Any

logger = logging.getLogger('config')


class ResultSet:
	"""
	Class which holds complex return types ( dict ) and include nice fetch methods like get(), etc.
	"""
	def __init__(self, data: dict):
		self.__data = data
		self.__keys = list(data.keys())

	def __len__(self):
		return len(self.__data)

	def raw(self) -> dict:
		"""Returns content of instance

		@return: Saved data
		"""
		return self.__data

	def get(self, key: str) -> Any:
		"""Returns value or ResultSet from key

		@param key: String with parameter name
		@return: Value under key

		@raise AttributeNotFoundError - Key not found
		"""
		if key not in self.__keys:
			raise AttributeNotFoundError(f"Key {key} not found as a parameter name")
		value = self.__data[key]
		if isinstance(value, dict):
			logger.debug(f"Returned ResultSet from key: {key}")
			return ResultSet(value)
		return value
