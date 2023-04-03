import re
import functools
import logging

from __decors import param, Converter

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


@Converter
def select_converter(*columns):
	return columns


@Converter
def distinct_converter():
	return True


class Query:

	pattern = Pattern

	def __init__(self, table: str):
		self.__table = table

		self.__where = []

	def where(self, *args) -> TQuery:
		self.__where.append(list(args))
		return self

	@param(converter=distinct_converter)
	def distinct(self) -> TQuery:
		return self

	@param(default="*", converter=select_converter)
	def select(self, *columns) -> TQuery:
		return self

	def ordered_by(self, column: str, method: Optional[str] = "desc") -> TQuery:
		pass

	@param
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
