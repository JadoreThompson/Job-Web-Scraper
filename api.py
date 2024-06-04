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
def all_apprenticeships(comp_name: Optional[str] = None, postcode: Optional[str] = None):
    conn, cur = get_conn_cur()

    def query_condition(query):
        db_query = f"""
                SELECT * FROM jobs
                WHERE comp_name='{query}';
                """
        cur.execute(db_query)
        rows = cur.fetchall()

        for row in rows:
            all_apps = [DbModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3])]

        cur.close()
        conn.close()

        return all_apps

    if comp_name is not None:
        return query_condition(comp_name)

    if postcode is not None:
        return query_condition(postcode)

    db_query = """
        SELECT * FROM jobs;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    all_apps = [DbModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3]) for row in rows]

    cur.close()
    conn.close()

    return all_apps


@app.get("/apprenticeships/{app_id}", response_model=DbModel)
def get_apprenticeship(app_id: int):
    conn, cur = get_conn_cur()

    db_query = f"""
        SELECT * FROM jobs 
        WHERE id='{app_id}' ;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    for row in rows:
        apprenticeship = DbModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3])

    cur.close()
    conn.close()

    return apprenticeship


if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=80, reload=True)
