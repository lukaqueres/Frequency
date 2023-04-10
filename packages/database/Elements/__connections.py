import psycopg2
import typing


TConnection = typing.TypeVar("TConnection", bound="Connection")


class Connection:

	def __init__(self):
		self.__url: str = "postgresql://postgres:postgres@localhost/postgres"
		self.__credentials: str = "dbname=postgres user=postgres password=postgres host=localhost port=5432"
		self.__conn: typing.Optional[psycopg2.connection] = None

	def __del__(self):
		if self.__conn:
			self.__conn.close()

	def url(self, url: str) -> TConnection:
		self.__url = url
		return self

	def string(self, credentials: str) -> TConnection:
		self.__credentials = credentials
		return self

	def connect(self) -> psycopg2.connection:
		self.__conn = psycopg2.connect()
		return self.__conn
