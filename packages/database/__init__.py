import logging
import doctest

try:
	import psycopg2
except ImportError:
	psycopg2 = None

from Query import Query

from Errors import Psycopg2NotInstalledError


if not psycopg2:
	raise Psycopg2NotInstalledError("psycopg2 required")

logger = logging.getLogger('database')
database_format = logging.Formatter('%(name)s - %(levelname)s : %(message)s')
database_handler = logging.StreamHandler()
database_handler.setLevel(logging.DEBUG)
database_handler.setFormatter(database_format)
logger.addHandler(database_handler)


def table(name: str) -> Query:
	query = Query(name)
	return query


class Connection:
	__url = "postgresql://postgres:postgres@localhost/postgres"

	@staticmethod
	def url(url: str):
		Connection.__url = url


if __name__ == "__main__":
	logger.debug(f"Performing doctests")
	doctest.testfile("doctest/doctests.txt", verbose=True)
