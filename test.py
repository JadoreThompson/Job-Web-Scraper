from models import get_conn_cur
from pydantic import BaseModel
from typing import Optional


class DbModel(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    postcode: Optional[str] = None
    comp_name: Optional[str] = None


conn, cur = get_conn_cur()

app_id = 1

db_query = f"""
    SELECT * FROM jobs 
    WHERE id={app_id} ;
"""

cur.execute(db_query)
rows = cur.fetchall()
if rows:
    print(rows)
else:
    print("DOG")

conn.commit()
cur.close()
conn.close()
