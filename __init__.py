import dash
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector as sql
import pandas as pd

app = dash.Dash()
app.title = 'Institut du Numérique Responsable'
db_connection = sql.connect(user='root', password='root', host='localhost', database='irn')
df = pd.read_sql('SELECT * FROM data', con=db_connection)
departments = df['Libdep']
newdata = pd.DataFrame()

def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app.layout = html.Div([
        html.Div(html.H1("Institut du Numérique Responsable"), style={"text-align":"center"}),
        html.Div(children=[
    html.H4(id='ForDept',children="Department"),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label':name, 'value':name} for name in departments],
            # value = list(fnameDict.keys())[0]
            value = departments[0]
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Br(),
        html.Div(children=[
    html.H4(id='ForPostal',children="Commune"),
        dcc.Dropdown(
            id='opt-dropdown',
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Hr(),
        html.Div(id='display-selected-values'),
        html.Br(),
        html.Div(id='TableData'),
        html.Br(),
        html.Div([
        html.Button(id='submit_button', n_clicks=0, children='Export'),
        html.Div(id='output_state')
    ])
])

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    com = df.loc[df['Libdep']== name]
    commune = com['Libcomm']
    return [{'label': i, 'value': i} for i in commune]

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def set_display_children(selected_value):
    return 'you have selected {} commune'.format(selected_value)

@app.callback(
    dash.dependencies.Output('TableData', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def set_generated_table(selected_value):

    if selected_value == None:
        return
    else:
        newdata = df.loc[df['Libcomm'] == selected_value]
        return html.Div(
        children=[generate_table(newdata)
            ])


@app.callback(
    dash.dependencies.Output('output_state', 'children'),
    [dash.dependencies.Input(component_id='submit_button', component_property='n_clicks')]
)
def update_output(num_clicks):
    if num_clicks > 0:
        newdata.to_csv("out.csv")
        return 'You have selected exported the data.'



server = app.server

if __name__ == '__main__':
    app.run_server()


