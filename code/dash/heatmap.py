import os
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash import Dash

YEARS = ['{}'.format(y) for y in range(2001, 2018)]

NEW_MEMBER_STATES = 'CZ HU PL SI SK LV LT HR BG RO'.split()
CANDIDATE_COUNTRIES = 'AL BA TR MK ME RS'.split()
NEIGHBORHOOD_COUNTRIES = 'DZ MA TN AM AZ GE MD UA'.split()
PARTNERS = 'RU CN US'.split() + CANDIDATE_COUNTRIES + NEIGHBORHOOD_COUNTRIES

country_codes = pd.read_csv("../../input/iso-3166/countries.csv")
export_data = pd.read_csv('../../output/TC_INDEX_EXP_.csv',index_col=0)
import_data = pd.read_csv('../../output/TC_INDEX_EXP_.csv',index_col=0)

export_data = export_data.merge(country_codes, how='left', left_on='DECLARANT', right_on='iso3166_2').rename(columns={'country_name': 'declarant_name'})
export_data = export_data.merge(country_codes, how='left', left_on='PARTNER', right_on='iso3166_2').rename(columns={'country_name': 'partner_name'})
export_data = export_data[export_data.PARTNER.isin(PARTNERS)]

def sort_data(Z):
    z = Z.values
    Z['sort'] = z.mean(axis=1)
    Z = Z.sort_values(by='sort', ascending=False).drop(columns='sort')
    return Z

def prepare_data(data, year):
    Z = sort_data(data.pivot(index='DECLARANT', columns='PARTNER', values='TCI_{}'.format(year)))

    z = Z.values
    x = Z.columns.values
    y = Z.index.values
    return (x, y, z)

app = Dash('')

layout = html.Div(
    [html.Div([html.H1("Trade Dissimilarity Index")], className="row", style={'textAlign': "center"}),
     html.Div(
         [dcc.Dropdown(id="selected-type", options=[{"label": i, "value": i} for i in YEARS],
                       value='2017',
                       style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"})],
         className="row"),
     html.Div([dcc.Graph(id="my-graph", style={"margin-right": "auto", "margin-left": "auto", "width": "80%"})],
              className="row")
     ], className="container")

app.layout = layout

@app.callback(
    Output("my-graph", "figure"),
    [Input("selected-type", "value")])

def update_figure(selected):
    x, y, z = prepare_data(export_data, selected)
    trace = go.Heatmap(x=x, y=y, z=z, colorscale='Electric', colorbar={"title": "KDL"}, showscale=True, zauto=False, zmin=0, zmax=12)
    return {"data": [trace],
            "layout": go.Layout(width=800, height=750, title=f"{selected.title()}", xaxis={"title": "Year"},
                                yaxis={"title": "Country", "tickmode": "array",
                                       "tickvals": export_data['declarant_name'].unique(),
                                       "ticktext": export_data['declarant_name'].unique(),
                                       "tickfont": {"size": 8}, "tickangle": -20}, )}

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
