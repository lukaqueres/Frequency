import doctest
import psycopg2
import os
import functools

from typing import Optional
from psycopg2 import sql


class ResultSet:
	def __init__(self, query: str, rows: list):
		self.__record = rows
		self.query = query
		self.index = 0

	@property
	def dump(self):
		dump = []
		for row in self.__record:
			dump.append(row.dump)
		return dump

	@property
	def num_rows(self):
		return len(self.__record)

	def __iter__(self):
		return self

	def __next__(self):
		if self.index == self.num_rows:
			raise StopIteration
		self.index += 1
		return self.__record[self.index]


class Row:
	def __init__(self, row: dict, query: Optional[str] = None):
		self.__record = row
		self.query = query

	@property
	def dump(self):
		return self.__record

	def get(self, key):
		return self.__record[key]


class Database:
	"""

	@version 0.1.0
	@author lukaqueres

	Example of usage:

	>>> db = Database(os.environ.get('DATABASE_URL'))

	>>> result = db.select("testing.guilds",["id", "name"], **{"prefix": "//", "name": "Wierd_'name-test\\""})
	>>> result.dump
	{'id': 2, 'name': 'Wierd_\\'name-test"'}
	>>> result = db.select("testing.guilds",["name", ], limit = None)
	>>> result.dump
	[{'name': 'Sample_name'}, {'name': 'Wierd_\\'name-test"'}]

	>>> db.insert("testing.guilds", **{"id": 10, "name": "Delete'\\"ted", "prefix": "/"})
	{'id': 10, 'name': 'Delete\\'"ted', 'prefix': '/'}
	>>> db.update("testing.guilds", {"name": "Changed\\"me", "prefix": "xd"}, **{"id": 10})
	1
	>>> result = db.select("testing.guilds",["name", "prefix"],**{"id": 10,})
	>>> result.dump
	{'name': 'Changed"me', 'prefix': 'xd'}
	>>> db.delete("testing.guilds", **{"id": 10})
	1

	@note psycopg2 documentation can be found here U{https://www.psycopg.org/docs/index.html}

	@note In case of transaction error call `con.rollback()`, use of `with` should (not) automatically take care of this

	"""
	url = os.environ.get('DATABASE_URL')
	con = None

	@staticmethod
	def with_connection(func):
		@functools.wraps(func)
		def wrapper_with_connection(*args, **kwargs):
			Database.__connect()
			result = func(*args, **kwargs)
			Database.con.close()
			return result

		return wrapper_with_connection

	def __init__(self, url: Optional[str] = None) -> None:
		"""

		@param url: Url used to connect to database in format: `postgresql://username:password@host:5432/database`
		"""
		self.con = psycopg2.connect(url or Database.url)
		self.url = url or Database.url

	def __del__(self):
		self.con.close()

	@staticmethod
	def __connect(url: Optional[str] = None):
		Database.con = psycopg2.connect(url or Database.url)

	@staticmethod
	def __disconnect():
		if Database.con:
			Database.con.close()

	@staticmethod
	@with_connection
	def select(table: str, columns: list, limit: None | int = 1, **constraints: dict) -> Row | ResultSet | None:
		"""Selects columns from specified table based on constraints

		@param table: Name of table, supports schemas
		@param columns: Tally of columns to be returned
		@param limit: limit selected rows to number, default 1
		@param constraints: Constraints limiting selection

		@return: Returns list / dict of row(s)
		"""
		query = "SELECT {columns} FROM {table} {where} {constraints} {limit}"
		data = {}
		cols = [sql.Identifier(c) for c in columns]
		formats = {"columns": sql.SQL(',').join(cols)}
		formats.update(table=sql.Identifier(*table.split(".", 2)))
		if constraints:
			formats.update(where=sql.SQL("WHERE"))
			i = 1
			conditions = {}
			for name, value in constraints.items():
				conditions.update({name: sql.Placeholder(f"constraint{i}{name}v")})
				data.update({f"constraint{i}{name}v": value})
				i += 1
			requisites = sql.SQL(" AND ").join(sql.SQL(" = ").join([sql.Identifier(n), v]) for n, v in conditions.items())
			formats.update(constraints=requisites)
		else:
			formats.update(where=sql.SQL(""), constraints=sql.SQL(""))
			pass
		formats.update(limit=sql.SQL("LIMIT 1" if limit else ""))
		with Database.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			if not curs.rowcount:
				return None
			if limit == 1:
				return Row(query=curs.query, row=dict(zip(columns, curs.fetchone())))
			else:
				rows = list(dict(zip(columns, r)) for r in curs.fetchall())
				return ResultSet(query=curs.query, rows=[Row(row=row) for row in rows])

	@staticmethod
	@with_connection
	def insert(table: str, **values: dict) -> dict:
		"""Insert row of values to given table

		@param table: Name of table, supports schemas
		@param values: Content of new row
		@return: Passed values
		"""
		query = "INSERT INTO {table} ( {columns} ) VALUES ( {values} )"
		formats = {"table": sql.Identifier(*table.split(".", 2))}
		formats.update(
			columns=sql.SQL(", ").join(sql.Identifier(c) for c in values.keys()))
		formats.update(
			values=sql.SQL(", ").join(sql.Placeholder(f"value{list(values).index(c)}{c}v") for c in values.keys()))
		data = {f"value{list(values).index(n)}{n}v": v for n, v in values.items()}
		with Database.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			Database.con.commit()
		return values

	@staticmethod
	@with_connection
	def update(table: str, values: dict, **constraints: dict) -> int:
		"""Update row(s) values based on constraints

		@param table: Name of table, supports schemas
		@param values: New values
		@param constraints: Limit number of affected rows
		@return: Number of affected rows
		"""
		query = "UPDATE {table} SET {values} WHERE {constraints}"
		formats = {"table": sql.Identifier(*table.split(".", 2))}
		formats.update(
			values=sql.SQL(", ").join(sql.SQL(" = ").join(
					[sql.Identifier(n), sql.Placeholder(f"value{list(values).index(n)}{n}v")]
				) for n, v in values.items()))
		formats.update(
			constraints=sql.SQL(", ").join(sql.SQL(" = ").join(
					[sql.Identifier(n), sql.Placeholder(f"constraint{list(constraints).index(n)}{n}v")]
				) for n, v in constraints.items()))
		data = {f"value{list(values).index(n)}{n}v": v for n, v in values.items()}
		data.update({f"constraint{list(constraints).index(n)}{n}v": v for n, v in constraints.items()})
		with Database.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			Database.con.commit()
			return curs.rowcount

	@staticmethod
	@with_connection
	def delete(table: str, **constraints: dict) -> int:
		"""Remove specified records from database

		@param table: Name of table, supports schemas
		@param constraints: Limits of deleted rows
		@return: Number of deleted rows
		"""
		query = "DELETE FROM {table} WHERE {constraints}"
		data = {}
		formats = {"table": sql.Identifier(*table.split(".", 2))}
		if not constraints:
			raise TypeError("Constraints can not be empty")
		i = 1
		conditions = {}
		for name, value in constraints.items():
			conditions.update({name: sql.Placeholder(f"constraint{i}{name}v")})
			data.update({f"constraint{i}{name}v": value})
			i += 1
		requisites = sql.SQL(" AND ").join(sql.SQL(" = ").join([sql.Identifier(n), v]) for n, v in conditions.items())
		formats.update(constraints=requisites)
		with Database.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			Database.con.commit()
			return curs.rowcount


doctest.run_docstring_examples(Database, globals())
