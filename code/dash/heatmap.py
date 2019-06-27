import os
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash import Dash

THETA = 8.0

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
    Z = Z.sort_values(by='sort', ascending=True).drop(columns='sort')
    return Z

def prepare_data(data, year):
    Z = sort_data(pd.np.exp(-1/THETA*data.pivot(index='declarant_name', columns='partner_name', values='TCI_{}'.format(year))))

    z = Z.values
    x = Z.columns.values
    y = Z.index.values
    return (x, y, z)

def update_slopechart(Partner):
    Declarants, Emphasized = NEW_MEMBER_STATES, []
    data = export_data[export_data.DECLARANT.isin(Declarants)].query('PARTNER=="{}"'.format(Partner))
    return {
        'data': [
        go.Scatter(
            x = [2001, 2017],
            y = [data.query('DECLARANT=="{}"'.format(d))['TCI_2001'].values[0], data.query('DECLARANT=="{}"'.format(d))['TCI_2017'].values[0]],
            text = 'Trade between {} and {}'.format(d, Partner),
            mode = 'lines',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'lightgrey'}
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


app = Dash('')

layout = html.Div([
      html.Div([
        html.H1("Trade Similarity Index"),

        dcc.Markdown('''
          ***
          ## Digital Revolution
          Bookstores, printers and publishers of newspapers and magazines
          have lost a combined 400,000 jobs since the recession began.
          Internet publishers — including web-search firms — offset
          only a fraction of the losses, adding 76,000 jobs.
          Electronic shopping and auctions made up the
           fastest-growing industry, tripling in employment in 10 years.
          ''', 
          className='container',
          style = {'maxWidth': '650px'}
        ),

        dcc.Dropdown(id="selected-year", options=[{"label": i, "value": i} for i in YEARS],
                   value='2017',
                   style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

        dcc.Graph(id="heatmap", style={"margin-right": "auto", "margin-left": "auto", "width": "80%"}),

        dcc.Markdown('''
          ***
          ## Digital Revolution
          Bookstores, printers and publishers of newspapers and magazines
          have lost a combined 400,000 jobs since the recession began.
          Internet publishers — including web-search firms — offset
          only a fraction of the losses, adding 76,000 jobs.
          Electronic shopping and auctions made up the
           fastest-growing industry, tripling in employment in 10 years.
          ''', 
          className='container',
          style = {'maxWidth': '650px'}
        ),

        dcc.Dropdown(id="selected-partner", options=[{"label": i, "value": i} for i in PARTNERS],
                   value='RU',
                   style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

        dcc.Graph(id="slopechart",
                style={"margin-right": "auto", "margin-left": "auto", "width": "60%"})],
                className="row"),

        ], style={'align': "center"})

app.layout = layout

@app.callback(
    Output("heatmap", "figure"),
    [Input("selected-year", "value")])

@app.callback(
    Output("slopechart", "figure"),
    [Input("selected-partner", "value")])

def update_figure(selected):
    x, y, z = prepare_data(export_data, selected)
    trace = go.Heatmap(x=x, y=y, z=z, colorscale='Electric', colorbar={"title": "KDL"}, showscale=True, zauto=False, zmin=0, zmax=1)
    return {"data": [trace],
            "layout": go.Layout(width=800, height=750, title=f"{selected.title()}", 
                                xaxis={"title": "Partner"},
                                yaxis={"title": "Reporter"} )}



if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
