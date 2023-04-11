import psycopg2
from psycopg2 import extensions

import typing

from urllib.parse import urlparse

TConnection = typing.TypeVar("TConnection", bound="Connection")


class Connection:

	def __init__(self):
		self.__url: str = "postgresql://postgres:postgres@localhost/postgres"
		self.__credentials: str = "dbname=postgres user=postgres password=postgres host=localhost port=5432"
		self.__conn: typing.Optional[extensions.connection] = None

	def __del__(self):
		if self.__conn:
			self.__conn.close()

	@property
	def connection(self):
		return self.__conn

	def url(self, url: str) -> TConnection:
		self.__url = url
		url = urlparse(url)
		credentials = ""
		credentials += f"user={url.username} "
		credentials += f"password={url.password} "
		credentials += f"dbname={url.path[1:]} "
		credentials += f"host={url.hostname} "
		credentials += f"port={url.port}"
		self.__credentials = credentials
		return self

	def string(self, credentials: str) -> TConnection:
		self.__credentials = credentials
		return self

	def connect(self) -> extensions.connection:
		self.__conn = psycopg2.connect(self.__credentials)
		return self.__conn
