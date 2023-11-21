import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import os

def lire_json_dossier(dossier):
    variables = set()
    for fichier in os.listdir(dossier):
        if fichier.endswith('.json'):
            chemin_complet = os.path.join(dossier, fichier)
            with open(chemin_complet, 'r') as file:
                data = json.load(file)
                for item in data:
                    variables.add(item['pointId'])
    return list(variables)

def extraire_donnees_variable(dossier, variable_selectionnee):
    timestamps = []
    valeurs = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.json'):
            chemin_complet = os.path.join(dossier, fichier)
            with open(chemin_complet, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item['pointId'] == variable_selectionnee and 'data' in item and 'value' in item['data']:
                        timestamps.append(item['timestamp'])
                        valeurs.append(item['data']['value'])
    return timestamps, valeurs

# Chemin vers le dossier contenant les fichiers JSON
dossier_json = 'data2'

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Liste des variables disponibles initialement
variables_disponibles = lire_json_dossier(dossier_json)

app.layout = html.Div([
    html.H1("Visualisation en Temps Réel des Données JSON"),
    dcc.Dropdown(
        id='variable-selector',
        options=[{'label': var, 'value': var} for var in variables_disponibles],
        value=variables_disponibles[0] if variables_disponibles else None
    ),
    dcc.Graph(id='live-data-graph'),
    dcc.Interval(
            id='interval-update',
            interval=5000,  # Mise à jour toutes les 5 secondes
            n_intervals=0
    )
])

@app.callback(
    [Output('live-data-graph', 'figure'),
     Output('variable-selector', 'options')],
    [Input('interval-update', 'n_intervals'),
     Input('variable-selector', 'value')]
)
def update_graph(n, selected_variable):
    variables_disponibles = lire_json_dossier(dossier_json)
    options = [{'label': var, 'value': var} for var in variables_disponibles]
    timestamps, valeurs = extraire_donnees_variable(dossier_json, selected_variable)
    figure = {
        'data': [go.Scatter(x=timestamps, y=valeurs, mode='lines+markers')],
        'layout': go.Layout(
            title=f'Variable: {selected_variable}',
            xaxis={'title': 'Timestamp'},
            yaxis={'title': 'Value'}
        )
    }
    return figure, options

if __name__ == '__main__':
    app.run_server(debug=True)
