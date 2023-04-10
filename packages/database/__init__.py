import logging
import doctest
import typing

try:
	import psycopg2
except ImportError:
	from __errors import Psycopg2NotInstalledError
	raise Psycopg2NotInstalledError("psycopg2 required")

from __query import Query
from __errors import NotConnectedError

from Elements.__connections import Connection

logger = logging.getLogger('database')
database_format = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
database_handler = logging.StreamHandler()
database_handler.setLevel(logging.DEBUG)
database_handler.setFormatter(database_format)
logger.addHandler(database_handler)


class Database:
	def __init__(self):
		self.__connection: typing.Optional[Connection] = None
		self.connection: typing.Optional[psycopg2.connection] = None

	def connect(self, url: typing.Optional[str]) -> None:
		self.__connection = Connection()
		self.connection = self.__connection.url(url).connect()

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


if __name__ == "__main__":
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)
