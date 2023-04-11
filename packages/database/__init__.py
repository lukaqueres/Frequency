import logging
import doctest
import typing

try:
	import psycopg2
	from psycopg2 import extensions
except ImportError:
	from _errors import Psycopg2NotInstalledError
	raise Psycopg2NotInstalledError("psycopg2 required")

from _query import Query
from _errors import NotConnectedError

from _elements.connections import Connection

logger = logging.getLogger('database')
database_format = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
database_handler = logging.StreamHandler()
database_handler.setLevel(logging.DEBUG)
database_handler.setFormatter(database_format)
logger.addHandler(database_handler)


class Database:
	def __init__(self):
		self.__connection: typing.Optional[Connection] = None

	@property
	def connection(self) -> extensions.connection | None:
		return None if not self.__connection else self.__connection.connection

	def connect(self, url: typing.Optional[str] = None, credentials: typing.Optional[str] = None) -> None:
		self.__connection = Connection()
		if url:
			self.__connection.url(url)
		else:
			self.__connection.string(credentials)
		self.__connection.connect()

	def table(self, name: str) -> Query:
		if not self.__connection:
			raise NotConnectedError("Connection must be set up before queries")
		query = Query(self, name)
		return query


__databases: dict[str, Database] = {}


def get(name: str) -> Database:
	if name in list(__databases.keys()):
		db = __databases[name]
	else:
		db = Database()
		__databases[name] = db
	return db


def dump(name: str) -> Database:
	if name in list(__databases.keys()):
		db = __databases[name]
		del __databases[name]
	else:
		raise KeyError("Database instance does not exists")  # TODO: Create nice error
	return db


if __name__ == "__init__":  # TODO: Temporary
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)

if __name__ == "__main__":
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)
