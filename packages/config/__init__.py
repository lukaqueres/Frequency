import json
import doctest
import logging
import os

try:
	import yaml
except ImportError:
	yaml = None

from typing import Any

from Errors import AttributeNotFoundError
from Errors import YamlNotInstalledError
from Errors import ExtensionNotSupportedError
from Result import ResultSet


class Config:
	"""
	@version 1.5.0

	Package used for configuration purposes.

	Can read from json or yaml files

	@note Yaml files support requires PyYAML package installed

	Contains built in logging support

	@author lukaqueres

	"""


logger = logging.getLogger('config')
config_format = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
config_handler = logging.StreamHandler()
config_handler.setLevel(logging.INFO)
config_handler.setFormatter(config_format)
logger.addHandler(config_handler)

if not yaml:
	logger.warning("PyYAML not installed. No yaml support included")

__data = {}
__keys = []


def save(data: dict) -> None:
	"""Saves passed key - value pairs. Note that value can be overwritten.

	@param data: dictionary with data to be saved.
	"""
	global __data, __keys
	__data.update(data)
	__keys += list(data.keys())
	logger.debug(f"Saved dict with {len(__keys)} keys")


def dump() -> dict:
	"""Returns and removes all saved data

	@return: saved records
	"""
	global __data, __keys
	data = __data
	__data = {}
	__keys = []
	return data


def get(key: str) -> Any | ResultSet:
	"""Returns value or ResultSet by provided key

	@param key: string key of value
	@return: parameter under key

	@raise AttributeNotFoundError: Key was not found
	"""
	global __data, __keys
	if key not in __keys:
		raise AttributeNotFoundError(f"Key {key} not found as a parameter name")
	value = __data[key]
	if isinstance(value, dict):
		logger.debug(f"Returned ResultSet from key: {key}")
		return ResultSet(value)
	logger.debug(f"Value returned {value} from key {key}")
	return value


def raw() -> dict:
	"""Method similar to dump() but returns data without removing it

	@return: currently stored data
	"""
	global __data, __keys
	logger.debug(f"Raw data returned")
	return __data


class File:
	"""
		Manages file reading from json and yaml files
	"""

	@staticmethod
	def json(file: str) -> dict:
		"""Retrieves data from json files

		@param file: Name of json file with data
		@return: Dictionary with file content
		"""
		global __data, __keys
		filename, file_extension = os.path.splitext(file)
		if file_extension != "json":
			raise ExtensionNotSupportedError("Method requires json file extension")
		try:
			with open(file, 'r') as c:
				content = json.load(c)
		except Exception as error:
			raise error
		logger.debug(f"Loaded json file: {file}")
		return content

	@staticmethod
	def yaml(file: str) -> dict:
		"""Retrieves data from yaml files. Requires PyYAML

		@param file: Name of yaml file with data
		@return: Dictionary with file content
		"""
		if not yaml:
			raise YamlNotInstalledError("Yaml files support requires PyYAML package installed")
		filename, file_extension = os.path.splitext(file)
		if file_extension != "yaml":
			raise ExtensionNotSupportedError("Method requires yaml file extension")
		try:
			with open(file, 'r') as c:
				content = c.read()
		except Exception as error:
			raise error
		logger.debug(f"Loaded yaml file: {file}")
		return yaml.safe_load(content)


if __name__ == "__main__":
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)
