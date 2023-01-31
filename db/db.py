import doctest
import psycopg2
import os

class Database():
    def __init__(self):
        self.con = self.__connect(os.environ.get('DATABASE_URL'))
        self.cur = self.cur(self.con)

    def __connect(self, url: str):

        return psycopg2.connect(url, sslmode='require')

    def __cur(self, con):
        return self.con.cursor()
