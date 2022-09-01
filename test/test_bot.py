import os
import psycopg2
from psycopg2.extensions import AsIs
from discord_bot.functions import get_time


def insert(table, payload):
    url = os.environ.get('DATABASE_URL')
    con = psycopg2.connect(url, sslmode='require')
    cur = con.cursor()
    columns = list(payload.keys())
    values = [payload[column] for column in columns]
    print(AsIs(table))
    print(columns[0])
    print(values[0])
    return cur.mogrify(
        "INSERT INTO %s (%s) VALUES (%s);",
        (AsIs(table), columns[0], values[0])
    )

def test_bot():
    assert str == type(get_time(specify="DT", return_type="str"))

def test_insert():
    payload = {"mycolumn": ["myvalue"]}
    query = insert("users", payload)
    assert query == b"INSERT INTO users ('mycolumn') VALUES (ARRAY['myvalue']);"
