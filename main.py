
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from typing import List

app = FastAPI()

#basemodel
class Voyage(BaseModel):
    name: str
    originpays: str
    vacancespays: str
    spentdays: str

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chaymae",
        password="chay",
        database="pays"
    )

#les voyages par pays
@app.get("/voyages/pays/{pays}", response_model=List[Voyage])
def get_voyages_by_pays(pays: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, originpays, vacancespays, spentdays FROM voyages WHERE vacancespays = %s", (pays,))
    voyages = cursor.fetchall()
    cursor.close()
    conn.close()
    return voyages

#les voyages par nom
@app.get("/voyages/personne/{name}", response_model=List[Voyage])
def get_voyages_by_personne(name: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, originpays, vacancespays, spentdays FROM voyages WHERE name = %s", (name,))
    voyages = cursor.fetchall()
    cursor.close()
    conn.close()
    return voyages

#everything
@app.get("/voyages", response_model=List[Voyage])
def get_all_voyages(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, originpays, vacancespays, spentdays FROM voyages LIMIT %s OFFSET %s", (limit, offset))
    voyages = cursor.fetchall()
    cursor.close()
    conn.close()
    return voyages

#stats
@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT vacancespays, COUNT(*) AS visites, AVG(CAST(spentdays AS DECIMAL)) AS avg_spentdays
        FROM voyages
        GROUP BY vacancespays
    """)
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return stats
