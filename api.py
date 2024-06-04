import uvicorn
import psycopg2

from pydantic import BaseModel
from fastapi import FastAPI
from models import get_conn_cur

from typing import Optional
from typing import List

app = FastAPI()
conn, cur = get_conn_cur()


class AppModel(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    postcode: Optional[str] = None
    comp_name: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "running successfully"}


@app.get("/apprenticeships", response_model=List[AppModel])
def all_apprenticeships(comp_name: Optional[str] = None, postcode: Optional[str] = None):

    def query_condition(query):
        db_query = f"""
                SELECT * FROM jobs
                WHERE comp_name='{query}';
                """
        cur.execute(db_query)
        rows = cur.fetchall()

        for row in rows:
            all_apps = [AppModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3])]

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

    all_apps = [AppModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3]) for row in rows]

    cur.close()
    conn.close()

    return all_apps


@app.get("/apprenticeships/{app_id}", response_model=AppModel)
def get_apprenticeship(app_id: int):
    conn, cur = get_conn_cur()

    db_query = f"""
        SELECT * FROM jobs 
        WHERE id='{app_id}' ;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    for row in rows:
        apprenticeship = AppModel(id=row[0], link=row[1], postcode=row[2], comp_name=row[3])

    cur.close()
    conn.close()

    return apprenticeship


@app.post("/create-apprenticeship")
def create_apprenticeship(apprenticeship: AppModel):
    db_query = """
        INSERT INTO jobs (link, postcode, comp_name)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """

    insert_value = [(apprenticeship.link, apprenticeship.postcode, apprenticeship.comp_name)]
    print(cur.executemany(db_query, insert_value))

    conn.commit()
    cur.close()
    conn.close()

    return apprenticeship

@app.put("/update-apprenticeship/{app_id}}")
def update_apprenticeship(app_id: int, apprenticeship: AppModel):
    db_query = f"""
        SELECT * FROM jobs 
        WHERE id='{app_id}' ;
    """
    if db_query:
        update_items = {
            "link": apprenticeship.link,
            "postcode": apprenticeship.postcode,
            "comp_name": apprenticeship.comp_name
        }

        fields_to_update = {k : v  for k, v in update_items.items() if v is not None}
        update_clause = ", ".join(f"{key} = '{value}'" for key, value in fields_to_update.items())
        db_query = f"""
            UPDATE jobs
            SET {update_clause}
            WHERE id = {app_id};
        """
        cur.execute(db_query)
        conn.commit()
        cur.close()
        conn.close()

        return apprenticeship

    else:
        return {"Message": "Didn't Update"}


@app.delete("/delete-apprenticeship")
def delete_apprenticeship(app_id: int):
    # values_dict = {}

    db_query = f"""
        SELECT * FROM jobs
        WHERE id = {app_id};
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    if rows:
        db_query = f"""
            DELETE FROM jobs
            WHERE id = {app_id};
        """
        cur.execute(db_query)
        conn.commit()
        cur.close()
        conn.close()

        return {"msg": "deleted"}

    else:
        return  {"msg": "ID doesn't exist"}







if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=80, reload=True)

