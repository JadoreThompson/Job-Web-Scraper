import uvicorn
import psycopg2

from pydantic import BaseModel
from fastapi import FastAPI
from models import get_conn_cur

from typing import Optional
from typing import List

app = FastAPI()


class DbModel(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    postcode: Optional[str] = None
    comp_name: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "running successfully"}


@app.get("/apprenticeships", response_model=List[DbModel])
def all_apprenticeships():
    conn, cur = get_conn_cur()

    db_query = """
        SELECT * FROM jobs;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    all_apps = [DbModel(link=row[1], postcode=row[2], comp_name=row[3]) for row in rows]

    conn.commit()
    cur.close()
    conn.close()

    return all_apps


@app.get("/apprenticeships/{task_id}")
def get_apprenticeship(task_id: int):
    conn, cur = get_conn_cur()

    db_query = f"""
        SELECT * FROM jobs 
        WHERE id='{task_id}' ;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    apprenticeship = [dict(zip([column[0] for column in cur.description], row)) for row in rows]

    conn.commit()
    cur.close()
    conn.close()

    return apprenticeship


if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=80, reload=True)
