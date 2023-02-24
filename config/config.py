import json
import os
import doctest
import logging.config

from typing import Any

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


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
	location = dir_path = os.path.dirname(os.path.realpath(__file__))

	def __init__(self, *files):
		"""
		Class for storing config data usage

		@param *files: Names of JSON files with configuration
		"""
		self.file_template = f"{Configuration.location}\\{{}}.json"
		self.saved = {}

		for name in files:
			self.__fetch(name)

		Configuration.instances.append(self)

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

	def __this_reload(self):
		"""Reloads values

		Simply fetches data again, overwriting previous fetch

		"""
		for name, values in self.saved.items():
			self.__fetch(name)

	@staticmethod
	def reload():
		"""Reloads every instance of Configuration class

		Reloads every instance of class from prepared list, calling `__this_reload()` function
		"""
		print(len(Configuration.instances))
		for instance in Configuration.instances:
			instance.__this_reload()


doctest.run_docstring_examples(Configuration, globals())
