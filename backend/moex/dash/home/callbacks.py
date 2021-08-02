from dash.dependencies import Input, Output
import plotly.graph_objs as go
from .layout import app
import pandas as pd
from moex.models import Issuer, Security, Price
from sklearn.linear_model import LinearRegression


@app.callback(
    [Output('security-dropdown', 'options'),
     Output('security-dropdown', 'value')],
    Input('issuer-dropdown', 'value')
)
def pull_securities(issuer_id):
    if issuer_id:
        issuer = Issuer.objects.filter(id=issuer_id).first()
        securities = issuer.securities.all()
        securities_list = [dict(label=security.code, value=security.id) for security in securities]
    else:
        securities_list = [dict(label=security.code, value=security.id) for security in Security.objects.all()]
    return securities_list, ''


@app.callback(
    Output('table-price', 'data'),
    Input('security-dropdown', 'value')
)
def pull_table(security):
    if security == '':
        return []
    prices = Price.objects.filter(security=security)
    return [dict(security=price.security.title, date=price.date, price=price.price) for price in prices]


@app.callback(
    Output('price-graph', 'figure'),
    Input('security-dropdown', 'value')
)
def pull_graph(security):
    if security == '':
        return []
    prices = Price.objects.filter(security=security)
    data_graph_x = [price.date for price in prices]
    data_graph_y = [price.price for price in prices]
    fig = go.Figure()

    model = LinearRegression()
    df_x = pd.DataFrame(data_graph_x)
    df_y = pd.DataFrame(data_graph_y)
    df_x[0] = pd.to_datetime(df_x[0])
    x = df_x[0].factorize()[0].reshape(-1, 1)
    y = df_y[0].values
    model.fit(x, y)
    fig.add_scatter(x=df_x[0].factorize()[0].tolist(), y=data_graph_y, name='line')
    moving_average = pd.DataFrame(dict(y=data_graph_y)).ewm(com=0.5).mean().values
    fig.add_scatter(x=df_x[0].factorize()[0].tolist(), y=[int(x) for x in moving_average], name='moving average')

    fig.add_scatter(x=df_x[0].factorize()[0].tolist(), y=model.predict(x), name='Lineal reg')
    fig.update_layout(
        xaxis=dict(
            tickmode='auto',
            tick0=data_graph_x[0]
        )
    )
    return fig

