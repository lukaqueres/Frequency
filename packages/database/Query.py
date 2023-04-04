import re
import functools
import logging

from __decors import Parameter
from __decors import Converter
from __decors import SubQuery

from typing import TypeVar
from typing import Optional
from typing import Any

from psycopg2 import sql

from Errors import InvalidColumnGiven

logger = logging.getLogger('database')

TQuery = TypeVar("TQuery", bound="Query")


class Pattern:
	"""
		SELECT documentation: https://www.postgresql.org/docs/current/sql-select.html
	"""

	select = "SELECT {distinct} {columns} FROM {table} WHERE {where} {order} {limit}"
	insert = "INSERT {values}"


class Result:
	pass


@Converter.set("select")
def select_converter(*args, **kwargs):
	kwargs["columns"] = {}
	for column in args:
		if not isinstance(column, str):
			continue
		if " as " in column:
			column = column.split()
			kwargs["columns"].update({column[0]: column[-1]})
		else:
			kwargs["columns"].update({column: column})
	return args, kwargs


@Converter.set("distinct")
def distinct_converter(*args, **kwargs):
	return args, kwargs


class Query:

	__select = SubQuery("select")

	def __init__(self, table: str):

		self.__table = table

		self.__where = []

	def where(self, *args) -> TQuery:
		self.__where.append(list(args))
		return self

	def distinct(self) -> TQuery:
		return self

	@Parameter.method
	@Converter.use("select")
	@Parameter.set(default={"columns": "*"})
	def select(self, *columns) -> TQuery:
		print(f"Columns: {columns}")
		return self

	def ordered_by(self, column: str, method: Optional[str] = "desc") -> TQuery:
		pass

	# @param
	def take(self, limit: int) -> TQuery:
		return self

	def get(self) -> Result:
		self.__construct("SELECT")
		pass

	def find(self, id_num: int) -> Result:
		pass

	def value(self, column: str) -> Any:
		pass

	def count(self):
		pass

	def max(self, column: str):
		pass

	def min(self, column: str):
		pass

	def avg(self, column: str):
		pass

	def sum(self, column: str):
		pass
