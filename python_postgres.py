import psycopg2


def get_cur():
    hostname = "localhost"
    database = "jobwebscraper"
    username = "postgres"
    pwd = "Jadore10@"
    port = 5432
    conn = None
    cur = None

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port
    )

    cur = conn.cursor()

    return cur

def get_conn():
    hostname = "localhost"
    database = "jobwebscraper"
    username = "postgres"
    pwd = "Jadore10@"
    port = 5432
    conn = None
    cur = None

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port
    )

    return conn


hostname = "localhost"
database = "jobwebscraper"
username = "postgres"
pwd = "Jadore10@"
port = 5432
conn = None

cur = None

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port
)

cur = conn.cursor()

create_tables = """
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    link varchar(255) NOT NULL UNIQUE,
    postcode varchar(40),
    comp_name varchar(40)
);
"""

cur.execute(create_tables)
insert_script = """
    INSERT INTO jobs (link, postcode, comp_name)
    VALUES (%s, %s, %s)
    ON CONFLICT (link) DO NOTHING;
"""

insert_values = [
    ("http://example.com/job1", "12345", "Company A"),
    ("http://example.com/job2", "67890", "Company B"),
    ("http://example.com/job3", "11111", "Company C"),
    ("http://examp[e.com/job4", "1234", "Company D")
]

cur.executemany(insert_script, insert_values)

conn.commit()
cur.close()

conn.close()