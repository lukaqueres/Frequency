import json
import doctest
from typing import Any


class Configuration:
	"""
	@version 0.1.0
	@author lukaqueres

	Example of usage:

	>>> configuration = Configuration("example")

	>>> configuration.get("example", "my.statement")
	'I like games'
	>>> print("About: ", configuration.get("example", "about_this_file"))
	About:  This is a test file for testing config.py file ( Specifically loading JSON values part )
	"""

	instances = []

	def __init__(self, *files):
		"""
		Class for storing config data usage

		@param *files: Names of JSON files with configuration
		"""
		self.file_template = "{}.json"
		self.saved = {}

		for name in files:
			self.__fetch(name)

	# noinspection PyTypeChecker
	def __fetch(self, name: str) -> None:
		"""Fetches content of JSON file and load in to parameter

		@type name: str
		@param name: Name of configuration file to load, also name for category
		"""

		file = self.file_template.format(name)
		try:
			with open(file, 'r') as c:
				content = json.load(c)
		except Exception as error:
			raise error
		else:
			self.saved[name] = content

	# noinspection PyTypeChecker
	def get(self, category: str, key: str) -> Any:
		""" Get provided key from selected category

		@type category: str
		@param category: Name of category
		@type key: str
		@param key: Key of specified value

		@return value: Returns value under provided key
		"""
		config = self.saved[category]
		keys = key.split('.')
		try:
			for key in keys:
				config = config[key]
		except Exception as error:
			raise error
		else:
			return config


doctest.run_docstring_examples(Configuration, globals())
