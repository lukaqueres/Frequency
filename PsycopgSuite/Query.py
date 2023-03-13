from psycopg2 import sql
import doctest

from Errors.PsycopgSuiteErrors import PsycopgSuiteValueError


class Query:
	def __init__(self):
		self.action = ""
		self.columns = []
		self.columns_aliases = {}
		self.where = []

	def select(self, *columns):
		if not columns:
			raise PsycopgSuiteValueError("No columns provided", str(columns))
		for column in columns:
			if column.isspace() or not column:
				raise PsycopgSuiteValueError("Invalid column string", str(columns))
			elif " " in column:
				column = column.split()
				if len(column) != 3 or column[1] != "as":
					raise PsycopgSuiteValueError("Invalid column string", column)
				self.columns.append(column[0])
				self.columns_aliases.update({column[0]: column[-1]})
			else:
				self.columns.append(column)
		return self

	def where(self, *args):
		if isinstance(args[0], Query):
			pass
		return self

	def get(self):
		pass

	def insert(self):
		pass

	def update_or_insert(self):
		pass

	def delete(self):
		pass
