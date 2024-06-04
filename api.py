import uvicorn
import psycopg2
from fastapi import FastAPI
from python_postgres import conn, cur

app = FastAPI()

def get_conn_cur():
    conn = psycopg2.connect(
        host="localhost",
        dbname="jobwebscraper",
        user="postgres",
        password="Jadore10@",
        port=5432
    )
    cur = conn.cursor()

    return conn, cur

@app.get("/")
def read_root():
    return {"message": "running successfully"}


@app.get("/apprenticeships")
def all_apprenticeships():
    conn, cur = get_conn_cur()

    db_query = """
        SELECT * FROM jobs;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    apprenticeships = [dict(zip([column[0] for column in cur.description], row)) for row in rows]

    conn.commit()
    cur.close()
    conn.close()

    return apprenticeships

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
