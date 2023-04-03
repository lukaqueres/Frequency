import re
import functools

from __decors import param, Converter, convert

from typing import TypeVar
from typing import Optional
from typing import Any

from psycopg2 import sql

from Errors import InvalidColumnGiven

TQuery = TypeVar("TQuery", bound="Query")


class Pattern:
	"""
		SELECT documentation: https://www.postgresql.org/docs/current/sql-select.html
	"""

	select = "SELECT {distinct} {columns} FROM {table} WHERE {where} {order} {limit}"
	insert = "INSERT {values}"


class Result:
	pass


@Converter
def select_converter(self):
	pass


class Query:

	pattern = Pattern

	def __init__(self, table: str):
		self.__table = table

		self.__distinct = False
		self.__limit = 0
		self.__order = ""

		self.__columns = {}

		self.__where = []

	def where(self, *args) -> TQuery:
		self.__where.append(list(args))
		return self

	def distinct(self) -> TQuery:
		self.__distinct = True
		return self

	@param(default="*", converter=select_converter)
	def select(self, *columns) -> TQuery:
		return self

	def ordered_by(self, column: str, method: Optional[str] = "desc") -> TQuery:
		pass

	def take(self, limit: int) -> TQuery:
		self.__limit = limit
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
