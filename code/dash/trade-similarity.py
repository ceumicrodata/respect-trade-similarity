# -*- coding: utf-8 -*-
import pandas as pd

import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask
from flask_cors import CORS
import os


country_codes = pd.read_csv("../../input/iso-3166/countries.csv")

export_data = pd.read_csv('../../output/TC_INDEX_EXP_.csv',index_col=0).query('PARTNER == "RU"')
import_data = pd.read_csv('../../output/TC_INDEX_EXP_.csv',index_col=0).query('PARTNER == "RU"')

export_data = export_data.merge(country_codes, how='left', left_on='DECLARANT', right_on='iso3166_2')
print(export_data.head())

'''
# Countries of focus
## New Member States
- Czech Republic
- Hungary
- Poland
- Slovenia
- Slovakia
- Latvia
- Lithuania
- Croatia
- Bulgaria
- Romania

## Candidate Countries
- Albania
- Bosnia
- Turkey
- Macedonia
- Montenegro
- Serbia

## Southern Neighbourhood Countries
- Algeria
- Morocco
- Tunisia

## Eastern Neighbourhood Countries
- Armenia
- Azerbaijan
- Georgia
- Moldova
- Ukraine
'''

NEW_MEMBER_STATES = 'CZ HU PL SI SK LV LT HR BG RO'.split()
CANDIDATE_COUNTRIES = 'AL BA TR MK ME RS'.split()
NEIGHBORHOOD_COUNTRIES = 'DZ MA TN AM AZ GE MD UA'.split()

series = {
    'export_index': {},
    'import_index': {},
    'meta': {},
}
for i in range(len(export_data)):
    export_meta = export_data.iloc[i, 0:2]
    #import_meta = import_data.iloc[i, 0:2]

    declarant, partner = export_meta.DECLARANT, export_meta.PARTNER
    key = (declarant, partner)

    export_row = export_data.iloc[i, 2:19]
    #import_row = import_row[df_wages.seriesid == cescode].iloc[0, 1:]

    # Collect data
    series['export_index'][key] = export_row
    series['meta'][key] = export_meta


def create_figure(highlight_country=None, skip_labels=[], show_only=[]):
    # Construct the charts
    scale = cl.scales['5']['div']['RdBu']
    traces = []
    annotations = []
    x = list(range(2001, 2018))
    for key in series['export_index'].keys():
        # Construct initial chart
        declarant, partner = key

        # convert growth over time to a relative scale and
        # jobs created across all industries to relative scale
        y = series['export_index'][key]
        growth = y[-1]

        if growth > 5:
            color = scale[4]
            legendgroup = '>5'
            name = 'Greater than 5'
        elif growth > 4:
            color = scale[3]
            legendgroup = '>4'
            name = 'Between 4 and 5'
        elif growth > 3:
            color = 'lightgrey'
            legendgroup = '>3'
            name = 'Between 3 and 4'
        elif growth > 2:
            color = scale[1]
            legendgroup = '>2'
            name = 'Between 2 and 3'
        else:
            color = scale[0]
            legendgroup = '<2'
            name = 'Less than 2'

        if highlight_country and declarant not in highlight_country:
            color = 'lightgrey'

        hoverinfo = 'text'
        width = 1
        if highlight_country and declarant in highlight_country:
            width = 2.5
            if color == 'lightgrey':
                color = 'grey'
            hoverinfo = 'text'
        elif highlight_country:
            width = 0.5
            hoverinfo = 'none'

        label = series['meta'][key].DECLARANT

        traces.append({
            'x': x,
            'y': y,
            'mode': 'lines',
            'line': {
                'color': color,
                'width': width
            },
            'text': [
                ('<b>{}</b><br>{}').format(
                    label,
                    year
                )
                for year in x
            ],
            'legendgroup': legendgroup,
            'name': name,
            'hoverinfo': hoverinfo,
            'showlegend': (
                False if legendgroup in [t['legendgroup'] for t in traces]
                else True
            )
        })

        if (highlight_country and declarant in highlight_country and
                (skip_labels and label not in skip_labels) or
                (show_only and label in show_only)):
            annotations.append({
                'x': traces[-1]['x'][-1], 'xref': 'x', 'xanchor': 'left',
                'y': traces[-1]['y'][-1], 'yref': 'y', 'yanchor': 'top',
                'showarrow': False,
                'text': label,
                'font': {'size': 12},
                'bgcolor': 'rgba(255, 255, 255, 0.5)'
            })

    # reorder traces to reorder legend items
    if not highlight_country:
        def get_trace_index(traces, legendgroup):
            for i, trace in enumerate(traces):
                if trace['showlegend'] and trace['legendgroup'] == legendgroup:
                    return i
        traces.insert(0, traces.pop(get_trace_index(traces, '<2')))
        traces.insert(0, traces.pop(get_trace_index(traces, '>2')))
        traces.insert(0, traces.pop(get_trace_index(traces, '>3')))
        traces.insert(0, traces.pop(get_trace_index(traces, '>4')))
        traces.insert(0, traces.pop(get_trace_index(traces, '>5')))
    else:
        # move highlighted traces to the end
        for i, trace in enumerate(traces):
            if trace['line']['width'] != 2.5:
                traces.insert(0, traces.pop(i))


    if not highlight_country:
        annotations = [{
            'x': 0.8, 'xref': 'paper', 'xanchor': 'left',
            'y': 0.95, 'yref': 'paper', 'yanchor': 'bottom',
            'text': '<b>Job Growth</b>',
            'showarrow': False
        }]

    layout = {
        'xaxis': {
            'showgrid': False,
            'showline': False,
            'zeroline': False,
            'showticklabels': False,
            'ticks': '',
            'title': '← Lower Wages        Industries        Higher Wages →'
        },
        'yaxis': {
            'showgrid': False,
            'showticklabels': False,
            'zeroline': False,
            'ticks': '',
            'title': 'Jobs'
        },
        'showlegend': not bool(highlight_country),
        'hovermode': 'closest',
        'legend': {
            'x': 0.8,
            'y': 0.95,
            'xanchor': 'left'
        },
        'annotations': annotations,
        'margin': {'t': 20, 'b': 20, 'r': 0, 'l': 20},
        'font': {'size': 12}
    }

    return {'data': traces, 'layout': layout}


app = Dash(__name__)
server = app.server

layout = html.Div([
    dcc.Markdown('''
    ***
    ## Digital Revolution
    Bookstores, printers and publishers of newspapers and magazines
    have lost a combined 400,000 jobs since the recession began.
    Internet publishers — including web-search firms — offset
    only a fraction of the losses, adding 76,000 jobs.
    Electronic shopping and auctions made up the
     fastest-growing industry, tripling in employment in 10 years.
    ''', className='container',
    style = {'maxWidth': '650px'}),

    dcc.Graph(
        figure=create_figure(NEW_MEMBER_STATES), id='media',
        style={'height': '90vh'}
    ),

    dcc.Markdown('''
    ***
    ## And More
    Discover patterns yourself by filtering through industries with
    the dropdown below.
    ''', className='container',
    style = {'maxWidth': '650px'}),

    html.Div(
        dcc.Dropdown(
            options=[
                {'label': c, 'value': c}
                for c in sorted(list(export_data.country_name.unique()))
            ],
            value=NEW_MEMBER_STATES,
            multi=True,
            id='category-filter',
        ), className='container', style={'maxWidth': '650px'}),
    html.Div(id='filtered-content'),

])


app.layout = layout


@app.callback(
    Output('filtered-content', 'children'),
    [Input('category-filter', 'value')])
def filter(selected_values):
    figure = create_figure(
        list(country_codes[
            country_codes.country_name.isin(selected_values)
        ].iso3166_2) if selected_values else None,
        skip_labels=['-'],
    )

    for trace in figure['data']:
        trace['hoverinfo'] = 'text'

    return dcc.Graph(
        id='filtered-graph',
        figure=figure
    )



if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
