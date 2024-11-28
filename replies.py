import pandas as pd
import requests
import mysql.connector
import io

url = "https://docs.google.com/spreadsheets/d/1B7wvIoamo7cv-QjmeE-OYRAtRn9O4qJ-juDOC2A6X5U/export?format=csv&gid=334701869"

response = requests.get(url, verify=False)
response.raise_for_status() 
data = response.content.decode('utf-8')
df = pd.read_csv(io.StringIO(data))

df.columns = df.columns.str.strip()

conn = mysql.connector.connect(
    host="localhost",        
    user="chaymae",          
    password="chay",         
    database="pays"          
)
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        SELECT COUNT(*) FROM voyages 
        WHERE name = %s 
        AND originpays = %s 
        AND vacancespays = %s 
        AND spentdays = %s
    """, (
        row['Nom ?'],                 
        row['votre pays d\'origine ?'],  
        row['Pays européens visités ?'],  
        row['Durée du séjour (Moyenne) dans chaque pays']  
    ))
    
    result = cursor.fetchone()
    
    if result[0] == 0:  # verif doublons
        cursor.execute("""
            INSERT INTO voyages (name, originpays, vacancespays, spentdays)
            VALUES (%s, %s, %s, %s)
        """, (
            row['Nom ?'],                 
            row['votre pays d\'origine ?'],  
            row['Pays européens visités ?'],  
            row['Durée du séjour (Moyenne) dans chaque pays']  
        ))

conn.commit()
cursor.close()
conn.close()





