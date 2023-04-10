import re
import functools
import logging

from __parameters import Parameter

from typing import TypeVar
from typing import Optional
from typing import Any

from psycopg2 import sql

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


class Query:

	def __init__(self, database, table: str):
		self.parameters = {}
		self.__database = database
		self.__table = table

		self.__where = []

	def where(self, *args) -> TQuery:
		self.__where.append(list(args))
		return self

	def distinct(self) -> TQuery:
		return self

	@Parameter.converter("select")
	@Parameter.set(name="select", default={"columns": "*"})
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
