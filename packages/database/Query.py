import re

from typing import TypeVar
from typing import Any
from typing import Optional

from Errors import InvalidColumnGiven

TQuery = TypeVar("TQuery", bound="Query")
TSelect = TypeVar("TSelect", bound="Select")


class Result:
	pass


class Query:
	def __init__(self):
		self.__table = None
		self.__where = {}

		self.columns = {}  # Select statement's
		self.distinct = False

	def table(self, name: str) -> TQuery:
		self.__table = name
		return self

	def select(self, *columns) -> TSelect:
		d_columns = {}
		for column in columns:
			if not (re.search("^\S+\sas\s\S+$", column) or re.search("^\S+$", column)):
				raise InvalidColumnGiven(f"Column `{column}` is invalid")
			if "as" in column:
				column = column.split()
				d_columns.update({column[0]: column[-1]})
			else:
				d_columns.update({column: column})

		select = Select(self.__table, d_columns)
		return select

	# -  (╯°□°)╯︵ ┻━┻  - FINISHERS

	def get(self) -> Result:
		select = Select(self.__table)
		return select.get()

	def find(self, with_id: int) -> Result:
		pass

	def count(self) -> int:
		pass

	# - Altering - ┬─┬ノ( º _ ºノ)

	def insert(self):
		pass

	def update(self) -> int:
		pass

	def update_or_insert(self) -> int:
		pass

	def delete(self) -> int:
		pass


class Select(Query):
	def __init__(self, table: Optional[str] = None, columns: Optional[dict] = None):
		super().__init__()
		if columns is None:
			columns = {}
		self.__table = table

		self.columns = columns
		self.distinct = False

	def select(self) -> None:
		pass

	def get(self) -> Result:
		pass
