import doctest
import psycopg2
import os
from typing import Any

# @link: https://www.psycopg.org/docs/index.html


class Database:
    def __init__(self):
        self.con = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
        self.cur = self.con.cursor()

    def select(self, table: str, columns: str | list, *constraints) -> Any:
        query = "SELECT %(columns)s FROM %(table)s WHERE %(constraints)s"
        data = {'columns': columns, 'table': table, 'constraints': constraints}
        self.cur(query, data)
        return self.cur.fetchall()

    def exists(self):
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
