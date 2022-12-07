from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv("crimedata.csv")
df.reset_index(drop=True, inplace=True)

df1 = df.groupby(['state']).agg(
    {"ViolentCrimesPerPop": "sum", 'nonViolPerPop': 'sum', "population": "sum"}).reset_index()
df1["CrimesPerPerson"] = (df1["ViolentCrimesPerPop"] + df1['nonViolPerPop']) / df1["population"]

fig1 = px.bar(df1, x="state", y="CrimesPerPerson")
fig1.update_layout(
    title={
        "text": "Распределение преступлений по штатам на человека",
    },
    xaxis_title="Штаты",
    yaxis_title="Значение",
    height=700,
    width=800
)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='crime_rate_by_state',
                figure=fig1)
        ],
            style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    ['murders', 'rapes', 'robberies', 'assaults', 'burglaries',
                     'larcenies', 'autotheft', 'arsons'],
                    'murders',
                    id='crime_type_dropdown'
                ),
                dcc.Graph(
                    id='crime_type'
                )
            ],
                style={'width': '49%', 'display': 'inline-block'})
        ]),
        html.Div([
            dcc.Dropdown(
                df['state'].unique(),
                'AK',
                id='state_dropdown'
            ),
            dcc.Graph(
                id='crime_type_by_state'
            ),
            dcc.Graph(
                id='race'
            ),

        ],
            style={'width': '49%', 'display': 'inline-block'})
    ]),

])


@app.callback(
    Output('crime_type', 'figure'),
    Input('crime_type_dropdown', 'value'))
def update(selected_type):
    df4 = df.groupby('state').agg({f'{selected_type}': 'sum'}).reset_index()
    fig4 = px.line(df4, x=df4['state'], y=df4[f'{selected_type}'])
    fig4.update_layout(
        title={
            "text": "Crime type by state",
            "x": 0.5,
        },
        height=350,
        xaxis_title="Вид преступления",
        yaxis_title="Значение",
    )
    return fig4


@app.callback(
    Output('race', 'figure'),
    Output("crime_type_by_state", 'figure'),
    Input('state_dropdown', 'value'))
def update(selected_state):
    df2 = df.copy(deep=True)
    for pct in ["racepctblack", 'racePctWhite', 'racePctAsian', 'racePctHisp']:
        df2[pct] = df2[pct] * df2['population'] / 100
    df2 = df2.groupby(["state"]).agg({"population": "sum", "racepctblack": "sum", "racePctWhite": "sum",
                                      "racePctAsian": "sum", "racePctHisp": "sum"}).reset_index()
    df2_state = df2[df2["state"] == selected_state].drop(labels=["population", "state"], axis=1).reset_index(drop=True)
    fig2 = px.pie(df2_state, names=["Black", "White", "Asian", "Hisp"], values=df2_state.loc[0])
    fig2.update_layout(
        title={
            "text": "Распределние по расам",
            "x": 0.5,
        },
        height=350
    )

    df3 = df.copy(deep=True)
    df3 = df3.groupby(["state"]).agg({"population": "sum", "murders": "sum", "rapes": "sum", "robberies": "sum",
                                      "assaults": "sum", "burglaries": "sum", "larcenies": "sum", "autoTheft": "sum",
                                      "arsons": "sum"}).reset_index()

    df3_state = df3[df3["state"] == selected_state].drop(labels=["population", "state"], axis=1).reset_index(drop=True)
    fig3 = px.bar(df3_state, x=['murders', 'rapes', 'robberies', 'assaults', 'burglaries',
                                'larcenies', 'autotheft', 'arsons'], y=df3_state.loc[0])
    fig3.update_layout(
        title={
            "text": "Распределение видов преступлений по штатам",
            "x": 0.5,
        },
        height=350,
        xaxis_title="Вид преступления",
        yaxis_title="Значение",
    )
    return fig2, fig3


if __name__ == '__main__':
    app.run_server()
