from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px
import pandas as pd
import requests

#API
api_url = "http://localhost:8000/voyages"
response = requests.get(api_url)
data = response.json()
df = pd.DataFrame(data)


total_days_per_country = df.groupby('vacancespays')['spentdays'].sum().reset_index()
total_days_per_country.rename(columns={'vacancespays': 'country', 'spentdays': 'total_days'}, inplace=True)

num_visitors_per_country = df.groupby('vacancespays')['name'].nunique().reset_index()
num_visitors_per_country.rename(columns={'vacancespays': 'country', 'name': 'num_visitors'}, inplace=True)

travel_connections = df.groupby(['originpays', 'vacancespays']).size().reset_index(name='num_trips')


app = Dash(__name__)

#layout
app.layout = html.Div([
    html.H1("cartes et tout ça", style={'textAlign': 'center'}),
    
    html.Div([
        html.H4("Select a map type to view:"),
        dcc.RadioItems(
            id='map-selector',
            options=[
                {'label': 'filter by nb de jours spent', 'value': 'days'},
                {'label': 'filter by nbr de visiteurs', 'value': 'visitors'},
                {'label': 'filter by travel connections', 'value': 'connections'}
            ],
            value='days',
            inline=True
        ),
        dcc.Graph(id='map-graph'),
    ]),
    
    html.Div([
        html.H4("Most Visited Countries by Origin:"),
        dcc.Dropdown(
            id='origin-dropdown',
            options=[{'label': country, 'value': country} for country in df['originpays'].unique()],
            value=df['originpays'].iloc[0]
        ),
        dash_table.DataTable(id='country-table', page_size=5),
    ]),
])


@app.callback(
    Output('map-graph', 'figure'),
    Input('map-selector', 'value')
)
def update_map(map_type):
    if map_type == 'days':
        fig = px.choropleth(
            total_days_per_country,
            locations='country',
            locationmode='country names',
            color='total_days',
            title='Total days Spent in each country',
            color_continuous_scale='Blues'
        )
    elif map_type == 'visitors':
        fig = px.choropleth(
            num_visitors_per_country,
            locations='country',
            locationmode='country names',
            color='num_visitors',
            title='Number of visitors in each country',
            color_continuous_scale='Greens'
        )
    elif map_type == 'connections':
        fig = px.line_geo(
            travel_connections,
            locations='originpays',
            locationmode='country names',
            line_group='vacancespays',
            title='Travel Connections',
            projection='natural earth'
        )
    else:
        fig = {}
    return fig

@app.callback(
    Output('country-table', 'data'),
    Input('origin-dropdown', 'value')
)
def update_table(origin_country):
    filtered_data = df[df['originpays'] == origin_country]
    return filtered_data[['vacancespays', 'spentdays']].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
