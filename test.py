from python_postgres import get_cur


cur = get_cur()

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
    ('http://trying.com', 'ABC123', 'PyTest')
]
print("All Values: ", insert_values)

cur.executemany(insert_script, insert_values)