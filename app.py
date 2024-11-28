from dash import Dash, html, dash_table
import pandas as pd
import requests
from io import StringIO

# Télécharger le fichier CSV en utilisant requests sans vérification SSL
url = 'https://docs.google.com/spreadsheets/d/1B7wvIoamo7cv-QjmeE-OYRAtRn9O4qJ-juDOC2A6X5U/export?format=csv&gid=334701869'
response = requests.get(url, verify=False)  

# Lire le contenu de la réponse dans un DataFrame pandas
data = StringIO(response.text)
df = pd.read_csv(data)

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
