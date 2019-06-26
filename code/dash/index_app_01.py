# coding=utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('../../output/TC_INDEX_EXP_.csv',index_col=0)
cc = pd.read_csv("../../input/iso-3166/countries.csv").set_index("iso3166_2")


def names(x):
    try: 
        return cc.loc[x]["country_name"]
    except: 
        return x


df.DECLARANT = df.DECLARANT.apply(names)
df.PARTNER = df.PARTNER.apply(names)


DECLARANTS = df["DECLARANT"].unique()
PARTNERS = df["PARTNER"].unique()



def part_num(x):
    if len(x)==1:
        return x
    elif len(x)>1:
        return [x]


app.layout = html.Div(children=[
    html.H1(children='Probe 01'),
    html.Div(children='''
        ceu microdata.
    '''),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='Declarants',
                options=[{'label': i, 'value': i} for i in DECLARANTS],
                value='HU',
                multi=True
            ),
            dcc.Dropdown(
                id='Partner',
                options=[{'label': i, 'value': i} for i in PARTNERS],
                value='RU',              
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='indicator-graphic'),
            ])
    ])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('Declarants', 'value'),
     Input('Partner', 'value'),
    ])

def update_graph(Declarants, Partner):
    return {
        'data': [
        go.Scatter(
            x = [x for x in range(2001,2018)],
            # danger zone: just map columns by their number, not their name
            y = df.loc[df.DECLARANT==d].loc[df.PARTNER==Partner, :].drop(columns=["DECLARANT","PARTNER"]).reset_index(drop=True).iloc[0,:].values,
            text = 'Trade between {} and {}'.format(d, Partner),
            mode = 'lines',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name = d
        )
        for d in Declarants],
        'layout': go.Layout(
            xaxis={
                'title': "Year",
            },
            yaxis={
                'title': "Dissimilarity",
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
