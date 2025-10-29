from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from numpy import sort

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Дашборд', style={'textAlign':'center'}),
    
    html.Div([

            html.P('Ось Y на линейном графике:'), 
            dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='dropdown-selection'),


            html.P('Страны для отображения на линейном графике:'),
            dcc.Checklist(df.country.unique(), ['Russia'], id='checklist-selection', inline=True),

        dcc.Graph(id='graph-content'),
        ]),

    html.Div([
        html.P('Ось Y для пузырьковой диаграммы:'),
        dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'lifeExp', id='bubble-dropdown-selection-y'),
        html.P('Ось X для пузырьковой диаграммы:'),
        dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'gdpPercap', id='bubble-dropdown-selection-x'),
        html.P('Размер для пузырьковой диаграммы:'),
        dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='bubble-dropdown-selection-size'),
        html.P('Год:'),
        dcc.Dropdown(sort(df.year.unique()), 1952, id='crossfilter-dropdown-selection-year'),
        html.Div([
            dcc.Graph(id='bubble-graph-content'),
            dcc.Graph(id='bar-graph-content'),
            dcc.Graph(id='pie-graph-content'),
            ], style={"display": "flex"})
        ])
]

@callback(
    Output('graph-content', 'figure'),
    Input('checklist-selection', 'value'),
    Input('dropdown-selection', 'value')
)
def update_graph(value1, value2):
    mask = df.country.isin(value1)
    return px.line(df[mask], x='year', y=value2, color='country', title='Линейный график по странам')

@callback(
    Output('bubble-graph-content', 'figure'),
    Input('crossfilter-dropdown-selection-year', 'value'),
    Input('bubble-dropdown-selection-y', 'value'),
    Input('bubble-dropdown-selection-x', 'value'),
    Input('bubble-dropdown-selection-size', 'value')
)
def update_graph(year, x, y, size):
    return px.scatter(df[df.year==year], x=x, y=y, size=size, color="country", hover_name="country", log_x=True, size_max=60, title='Пузырьковая диаграмма')

@callback(
    Output('bar-graph-content', 'figure'),
    Input('crossfilter-dropdown-selection-year', 'value')
)
def update_graph(year):
    dff = df[df.year==year]
    return px.bar(dff.sort_values(by=['pop'], ascending=False)[:15], x='country', y='pop', title='Топ 15 стран по популяции')

@callback(
    Output('pie-graph-content', 'figure'),
    Input('crossfilter-dropdown-selection-year', 'value')
)
def update_graph(year):
    dff = df[df.year==year]
    dff = dff.groupby('continent').sum()
    return px.pie(pd.concat([dff, pd.Series(data=list(dff.index), index=dff.index, name='continent')], axis=1), values='pop', names='continent', title='Круговая диаграмма по популяции на континентах')

if __name__ == '__main__':
    app.run(debug=True)
