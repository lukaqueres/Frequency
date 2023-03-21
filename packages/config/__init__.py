import json
import doctest
import logging

from typing import Any

from Errors import AttributeNotFoundError
from Result import ResultSet


logger = logging.getLogger('config')
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s : %(message)s')


__data = {}
__keys = []


def load_json(file) -> bool:
	global __data, __keys
	try:
		with open(file, 'r') as c:
			content = json.load(c)
	except Exception as error:
		raise error
	else:
		__data.update(content)
		__keys = list(content.keys())
	logger.debug(f"Loaded file {file} with {len(__keys)} keys")
	return True


def get(key) -> Any | ResultSet:
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
	global __data, __keys
	logger.debug(f"Raw data returned")
	return __data


if __name__ == "__main__":
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)
