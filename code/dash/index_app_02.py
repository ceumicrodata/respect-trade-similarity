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

cc = pd.read_csv("../../output/CC_detail.csv").set_index("ISO_code")

gdp = pd.read_csv("../../output/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_10576699.csv").rename(columns = {"Country Name":"Country_Name"})


def names(x):

    try: 
        return cc.loc[x]["c_name"]
    except: 
        return x

cc.GDP_by_capita = cc.GDP_B_USD/cc.pop


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
                id='Declarant',
                options=[{'label': i, 'value': i} for i in DECLARANTS],
                value='HU',
                multi=True
            ),
            dcc.Dropdown(
                id='Parners',
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
    [Input('Declarant', 'value'),
     Input('Parners', 'value'),
    ])

def update_graph(Declarant, Partners):
    #print(df.loc[df.DECLARANT==Declarant].loc[df.PARTNER==Parners[0], :])

    return {

        'data': [[


        go.Scatter(
            x=[x for x in range(2001,2018)],
            y=df.loc[df.==d].loc[df.PARTNER==Partners, :].drop(columns=["DECLARANT","PARTNER"]).reset_index(drop=True).iloc[0,:].values,
            text= "Trade between",
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name = d
        )

       for d in Declarant],

        [go.Scatter(
            x=[x for x in range(2001,2017)],
            y=gdp.loc[gdp.Country_Name==d].drop(columns=["Country_Name"]).reset_index(drop=True).iloc[0,:].values,
            text= "Trade between",
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name = d
        )

       for d in Declarant]],


        'layout': go.Layout(
            xaxis={
                'title': "Year",
            },go.Bar(
    x=['giraffes', 'orangutans', 'monkeys'],
    y=[20, 14, 23],
    name='SF Zoo'
)
            yaxis={
                'title': "Country",
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
