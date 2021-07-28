import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from django_plotly_dash import DjangoDash
from moex.models import Issuer

app = DjangoDash('Home')


app.layout = html.Div([
    dcc.Store(id='store'),
    html.Div([
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[dict(label=issuer.title, value=issuer.id) for issuer in Issuer.objects.all()],
            value=''
        ),
        dcc.Dropdown(
            id='security-dropdown',
            options=[],
            value='',
            style={'margin-top': '20px'}
        ),
    ], style={'width': '200px'}),
    html.Div([
        html.H3(['Table price'], style={}),
        html.Div([
            dash_table.DataTable(
                id='table-price',
                columns=[dict(name='security', id='security'),
                         dict(name='price', id='price'),
                         dict(name='date', id='date')],
                data=[],
                page_size=20,
                style_table={'width': '600px'}),
        ])
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
    html.Div([
        html.H3(['history by current security']),
        dcc.Graph(
            id='price-graph',
            figure=go.Figure(),
            style={'width': '1000px'}
        ),
    ], style={'margin-top': '40px', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

], style={'display': 'flex', 'flex-direction': 'column'})

