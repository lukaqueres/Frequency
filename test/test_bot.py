import os
import psycopg2
from psycopg2.extensions import AsIs
from discord_bot.functions import get_time


def get_insert_query(table, payload):
    url = os.environ.get('DATABASE_URL')
    con = psycopg2.connect(url, sslmode='require')
    cur = con.cursor()
    columns = list(payload.keys())
    values = [payload[column] for column in columns]
    return cur.mogrify(
        "INSERT INTO %s %s VALUES %s;",
        (AsIs(table), tuple(columns), tuple(values))
    )

def test_bot():
    assert str == type(get_time(specify="DT", return_type="str"))

def test_insert_one_value():
    payload = {"mycolumn": ["myvalue"]}
    query = get_insert_query("users", payload)
    assert query == \
        b"INSERT INTO users ('mycolumn') " \
        b"VALUES (ARRAY['myvalue']);"

def test_insert_two_columns():
    payload = {
        "mycolumn": ["myvalue"],
        "mycolumntwo": ["myvaluetwo"]
    }
    query = get_insert_query("users", payload)
    expected_query = \
        b"INSERT INTO users ('mycolumn', 'mycolumntwo') " \
        b"VALUES (ARRAY['myvalue'], ARRAY['myvaluetwo']);"
    assert expected_query == query
