import pandas as pd
import yfinance as yf
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import numpy as np 

#-----------------------------------------------------------------------------------
# DATA
#-----------------------------------------------------------------------------------

# Extraccion de los datos 
w = [1/3,1/3,1/3]
tickers = ['MSFT', 'AAPL', 'META']
df = pd.DataFrame({'Weights':w, 'Tickers':tickers}).round(3)
data = yf.download(tickers = tickers, start = '2020-01-01', end = '2022-11-10', interval = '1wk')
data_m = yf.download(tickers = tickers, start = '2020-01-01', end = '2022-11-10', interval = '1mo')


#Calculos 
roi = (data['Adj Close'].pct_change().fillna(0) + 1).cumprod()
roi['PORTFOLIO'] = np.dot(roi.to_numpy(),w)

roi_m=(data_m['Adj Close'].pct_change().fillna(0))
roi_m['PORTFOLIO'] = np.dot(roi_m.to_numpy(),w)

#Figuras 
fig = px.line(roi['PORTFOLIO'],log_y=False, title = 'Portfolio Returns'); fig.update_layout(showlegend=False)
fig2 = px.pie(df,values = 'Weights', names = 'Tickers', title = 'Portfolio Allocation')
fig3 = px.line(roi, title = 'Stocks & Portfolio Returns')
fig4 = px.bar(roi_m['PORTFOLIO'], title = 'Monthly Portfolio Returns'); fig4.update_traces(width=1000000000);fig4.update_layout(showlegend=False)

#-----------------------------------------------------------------------------------
# DASHBOARD
#-----------------------------------------------------------------------------------

app = Dash(__name__)
server = app.server

#colors = {
    #'background': '#111111',
    #'text': '#7FDBFF'
#}

app.layout = html.Div(
    #Colores de la app:
    #style={'backgroundColor': colors['background']},

    #Elementos de la app (titulos, figuras, graficos...):
    children=[
    
    #TITULOS Y TEXTOS 
    html.H1('DASHBOARD DEL UPVIC',style={'textAlign': 'center'}),
    html.Div('Bienvenido al dashboard del portfolio del UPVIC.',style={'textAlign': 'center'}),

    #GRÁFICOS Y TABLAS 
    dcc.Graph(figure=fig, style={'display': 'inline-block'}),
    dcc.Graph(figure=fig2, style={'display': 'inline-block'}),
    dcc.Graph(figure=fig3, style={'display': 'inline-block'}),
    dcc.Graph(figure=fig4, style={'display': 'inline-block'})

])
#'width': '50vw', 'height': '90vh'

if __name__ == '__main__':
    app.run_server(debug=True)
