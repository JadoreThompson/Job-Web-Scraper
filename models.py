import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')


def get_conn_cur():
    conn = psycopg2.connect(
        host=os.getenv('HOSTNAME'),
        dbname=os.getenv('DATABASE'),
        user=os.getenv('UNAME'),
        password=os.getenv('PASSWORD'),
        port=os.getenv('PORT')
    )
    cur = conn.cursor()

    return conn, cur


conn, cur = get_conn_cur()

create_tables = """
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    link varchar(255) NOT NULL UNIQUE,
    postcode varchar(40),
    comp_name varchar(40)
);
"""
cur.execute(create_tables)

# THE TEST BELOW WORKS
# insert_script = """
#     INSERT INTO jobs (link, postcode, comp_name)
#     VALUES (%s, %s, %s);
# """
#
# insert_values = [
#     ('placeholder', 'placeholder', 'placeholder')
# ]
#
# cur.executemany(insert_script, insert_values)

conn.commit()
cur.close()
conn.close()
