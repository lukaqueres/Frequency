from psycopg2 import sql
import doctest

from Errors.PsycopgSuiteErrors import PsycopgSuiteValueError  # raise PsycopgSuiteValueError("No columns provided", str(columns))


class Table:
	def __init__(self):
		return Query()


class Query:
	"""
	>>> Query("test_guild").get()
	"""
	def __init__(self, name):
		self.name = name
		self.columns = []

	def get(self):
		pass  # TODO: Execute generated query

	def first(self):
		pass

	def find(self):
		pass

	def where(self):
		pass

