from models import get_conn_cur
from pydantic import BaseModel
from typing import Optional


class DbModel(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    postcode: Optional[str] = None
    comp_name: Optional[str] = None


conn, cur = get_conn_cur()

db_query = """
    SELECT * FROM jobs;
"""
cur.execute(db_query)
rows = cur.fetchall()
print("All Rows: ", rows)

i = 0
all_apps = [DbModel(link=row[1], postcode=row[2], comp_name=row[3]) for row in rows]
print(all_apps)

conn.commit()
cur.close()
conn.close()
