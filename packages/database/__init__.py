import logging
import doctest

try:
	import psycopg2
except ImportError:
	from Errors import Psycopg2NotInstalledError
	raise Psycopg2NotInstalledError("psycopg2 required")

from __query import Query

from Elements.__connections import Connection

logger = logging.getLogger('database')
database_format = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
database_handler = logging.StreamHandler()
database_handler.setLevel(logging.DEBUG)
database_handler.setFormatter(database_format)
logger.addHandler(database_handler)


class Database:
	def __init__(self):
		self.__connection: Connection

	def table(self, name: str) -> Query:
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
