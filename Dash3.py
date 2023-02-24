import pandas as pd
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import plotly_express as px
import plotly.graph_objects as go



data = {}
with open(os.path.join(os.getcwd(), 'variables2.txt'), 'r') as f:
    for line in f:
        name, value = line.strip().split('=')
        data[name] = value
new_path = str(data.get('new_path'))
final_path = str(data.get('final_path'))

path = new_path
path = path.replace(os.sep, "/")

print(path)


#create a dashboard class and store all of it
#driver file and create instance of both classes
#in the init function have parameters that take in the GUI and pass them to the dashboard

#driver will serve as main function


def read_population_data(path):
    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    df_list = []
    for file in files:
        df = pd.read_csv(os.path.join(path, file))
        if 'WWWW' in df.columns:
            df = df.drop(columns=['Time', 'Patch', 'WWWR', 'WRWW', 'WRWR', 'WRRR', 'RRWW', 'RRWR'])
            df = df.rename(columns={"WWWW": "Wildtype", "WWRR": "Heterozygote", "RRRR": "pgSIT"}, errors="raise")
        else:
            df = df.drop(columns=['Time', 'Patch'])
            df = df.rename(columns={"WW": "Wildtype", "WR": "Heterozygote", "RR": "pgSIT"}, errors="raise")

        df['sum'] = df.sum(axis=1)
        df_list.append(df)

    df = pd.concat(df_list)

    df_grouped = df.groupby(df.index // 62).sum()
    df_grouped['Time2'] = [7 * i for i in range(len(df_grouped))]
    df_melt = df_grouped.melt(id_vars='Time2', var_name='Genotype', value_name='sum1')
    return df_melt

image_path = 'assets/logo.png'

# Define the app layout
app = dash.Dash(__name__)

app.layout = html.Div(
    style = {
        'margin': '15px'
    },
    children =

    [

        html.H1("Mosquito Sim Dashboard V1.0", style={"font-family": "Helvetica", "text-align": "left", "color": "#5a9ed5"}),
        html.H6("Mosqutio Population Dynamics on Onetahi Island", style={"font-family": "Helvetica", 'font-weight':'100', "text-align": "left", "color": "#5a9ed5"}),
        html.Img(
            src=image_path,
            style={
                'position': 'absolute',
                'top': '10px',
                'right': '170px',
                'margin': '15px',
                'height': '100px'
            }
        ),

        html.Div(
            [
                html.Div(
                    style={
                        "background-color": "#2ad9a8",
                        "height": "45px",
                        "width": "12px",
                        "margin-right": "8px"
                    }
                ),
                dcc.Dropdown(
                    id="folder-dropdown",
                    options=[
                        {
                            "label": f,
                            "value": os.path.join(new_path, f),
                        }
                        for f in sorted(os.listdir(new_path))
                        if os.path.isdir(os.path.join(new_path, f))
                    ],
                    value=final_path,
                    style={
                        "width": "60%",
                        "color": "#000000",
                        "padding": "2px",
                        "margin-bottom": "5px",
                    },


                )
            ],
            style={
                "display": "flex",
                "justify-content": "left",
                "align-items": "left",
                "padding-top": "20px",
                "padding-bottom": "20px",
                "margin-bottom": "50px",
            },
        ),

        dcc.Interval(
            id='dropdown-update-interval',
            interval=5000,  # in milliseconds
            n_intervals=0
        ),

        dcc.Interval(
            id='graph-update-interval',
            interval=5000,  # in milliseconds
            n_intervals=0
        ),

        html.Div(
        [
            html.H6("Local Population Over Time",
            style={"font-family": "Helvetica", "color": "#2ad9a8", "text-align": "left"}),
            dcc.Graph(id="population-graph"),
            html.Div(style={"height": "10px", "margin-top": "20px"}),
        ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "width": "60%",
                "border": "1px solid #252e3f",
                "background-color": "#252e3f",
                "padding": "20px",
                "height": "70vh"
            }
        ),
        html.Div(
            [
                html.Div(
                    id="summary-stats",
                    style={
                        "font-family": "Helvetica",
                        "color": "#2c74c3",
                        "border": "1px solid #252e3f",
                        "background-color": "#252e3f",
                        "padding": "10px",
                        "margin-top": "160px",
                        "height": "500px",
                        "width": "300px"
                    }
                ),
                html.Div(
                    id="effect-sizes",
                    style={
                        "font-family": "Helvetica",
                        "background-color": "#252e3f",
                        "color": "#2c74c3",
                        "border": "1px solid #252e3f",
                        "padding": "15px",
                        "margin-top": "20px",
                        "height": "450px",
                        "width": "300px"
                    }
                )
            ],
            style={
                "position": "absolute",
                "top": "50px",
                "right": "100px",
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center"
            }
        )
    ]
)



@app.callback(
    Output("folder-dropdown", "options"),
    [Input("dropdown-update-interval", "n_intervals")]
)
def update_folder_dropdown_options(n):
    # update the list of directories in the dropdown
    folder_options = [
        {
            "label": f,
            "value": os.path.join(new_path, f),
        }
        for f in sorted(os.listdir(new_path))
        if os.path.isdir(os.path.join(new_path, f))
    ]
    return folder_options


def update_population_graph_data(path):
    return read_population_data(path)


@app.callback(
    Output("population-graph", "figure"),
    [Input("folder-dropdown", "value"), Input("graph-update-interval", "n_intervals")]
)


def update_population_graph(path, n_intervals):
    df = update_population_graph_data(path)

    layout = dict(
        plot_bgcolor="#252e3f",
        paper_bgcolor="#252e3f",
        xaxis=dict(
            title="Time (days)",
            tickfont=dict(color="#2ad9a8"),
            gridcolor="#29d88f",
            title_font=dict(color="#2ad9a8")
        ),
        yaxis=dict(
            title="# Mosquitoes",
            tickfont=dict(color="#2ad9a8"),
            showgrid=True,
            gridcolor="#2ad9a8",
            title_font=dict(color="#2ad9a8")
        ),
        font=dict(color="#2ad9a8"),
        margin=dict(t=10, b=10, l=10, r=10)
    )

    fig = px.line(
        df,
        x="Time2",
        y="sum1",
        color="Genotype",
        template="plotly_dark"
    )

    fig.update_layout(layout)
    fig.update_layout(
        width=800,
        height=800,
        #margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="#252e3f",
        plot_bgcolor="#252e3f",
        legend=dict(font=dict(color="#2ad9a8"))
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#2ad9a8")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#2ad9a8")

    fig.update_layout(
        xaxis_title="Time (days)",
        yaxis_title="# Mosquitoes",
        legend_title="Genotype",
    )

    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=.89,
            xanchor="right",
            x=1.25,
            bgcolor='#252e3f'
        )
    )

    fig.update_traces(
        line=dict(width=2)
    )

    fig.update_layout(shapes=[
        dict(
            type='rect',
            xref='x',
            yref='y',
            x0=df['Time2'].min(),
            y0=df['sum1'].min(),
            x1=df['Time2'].max(),
            y1=df['sum1'].max(),
            fillcolor='rgba(128,128,128,0.1)',
            opacity=0.5
        )
    ])

    return fig

@app.callback(
Output('summary-stats', 'children'),
Input('folder-dropdown', 'value'),
)


def update_summary_stats(path):
    df = read_population_data(path)

    data = {}
    with open(os.path.join(os.getcwd(), 'variables2.txt'), 'r') as f:
        for line in f:
            name, value = line.strip().split('=')
            data[name] = value

    rel_num = int(data.get('rel_num'))
    rel_val = float(data.get('rel_val'))
    dim = str(data.get('new_path'))
    dim = os.path.basename(dim)
    rel_srt = int(data.get('rel_srt'))
    rel_int = int(data.get('rel_int'))






# Return the updated content for the summary stats box
    return [
        html.H2('Release Values', style={'font-family': 'Helvetica', 'text-align': 'center'}),
        html.P([
            html.Sup(f'{rel_num}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight':'500', 'font-family': 'sans-serif','color': '#2ad9a8'}),
            html.Br(),
            html.Span('Number of Releases', style={'font-size': '1.0em'}),
        ], style={'text-align': 'center'}),
        html.P([
            html.Sup(f'{rel_val}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight': '500', 'font-family': 'sans-serif', 'color': '#2ad9a8'}),
            html.Br(),
            html.Span('Release Proportion', style={'font-size': '1.0em'}),
        ], style={'text-align': 'center'}),



        html.P([
            html.Sup(f'{rel_int}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight': '500',
                                      'font-family': 'sans-serif', 'color': '#2ad9a8'}),
            html.Br(),
            html.Span('Time between Releases', style={'font-size': '1.0em'}),
        ], style={'text-align': 'center'}),
        html.P([
            html.Sup(f'{rel_srt}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight': '500',
                                      'font-family': 'sans-serif', 'color': '#2ad9a8'}),
            html.Br(),
            html.Span('Release Start', style={'font-size': '1.0em'}),
        ], style={'text-align': 'center'}),
        html.P([
            html.Sup(f'{dim}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight': '500',
                                      'font-family': 'sans-serif', 'color': '#2ad9a8'}),
            html.Br(),
            html.Span('Output Folder Name', style={'font-size': '1.0em'}),
        ], style={'text-align': 'center'}),

    ]


@app.callback(
Output('effect-sizes', 'children'),
Input('folder-dropdown', 'value')
)
def update_effect_sizes(path):
    data = {}
    with open(os.path.join(os.getcwd(), 'variables2.txt'), 'r') as f:
        for line in f:
            name, value = line.strip().split('=')
            data[name] = value

    rel_num = int(data.get('rel_num'))

    # Read the data from the given path
    df_melt = read_population_data(path)
    wildtype_df = df_melt[df_melt["Genotype"] == "Wildtype"]
    first_wildtype = wildtype_df.iloc[0]["sum1"]
    last_wildtype = wildtype_df.iloc[-1]["sum1"]
    ad_pop_eq = first_wildtype

    change = (last_wildtype - first_wildtype) / first_wildtype
    change = change *100



    # Calculate the Total Releases
    total_releases = df_melt[df_melt['Genotype'] == 'pgSIT']['sum1'].sum()
    per_rel = total_releases/rel_num
    per_rel = round(per_rel)

# Create the HTML elements for displaying the effect sizes
    children =[html.H2('Effect Sizes', style={'font-family': 'Helvetica', 'text-align': 'center'}),    html.P([        html.Sup(f'{ad_pop_eq}', style={'color': '#2ad9a8','font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight':'500', 'font-family': 'sans-serif'}),        html.Br(),        html.Span('Starting Wildtype Pop', style={'font-size': '1.0em'})    ], style={'text-align': 'center'}),
    html.P([html.Sup(f'{last_wildtype}', style={'font-size': '1.7em', 'margin-top': '-0.5em', 'font-weight':'500', 'font-family': 'sans-serif', 'color': '#2ad9a8'}),        html.Br(),        html.Span('Final Wildtype Pop', style={'font-size': '1.0em'})    ], style={'text-align': 'center'}),
    html.P([html.Sup(f'{change:.2f}%', style={'font-size': '1.7em', 'margin-top': '-0.5em','font-weight':'500', 'font-family': 'sans-serif','color':'#2ad9a8'}),        html.Br(),        html.Span('Percent Change in WT Population', style={'font-size': '1.0em'})    ], style={'text-align': 'center'}),
    html.P([html.Sup(f'{per_rel}', style={'font-size': '1.7em', 'margin-top': '-0.5em','font-weight':'500', 'font-family': 'sans-serif','color':'#2ad9a8'}),        html.Br(),        html.Span('pgSIT per Release', style={'font-size': '1.0em'})    ], style={'text-align': 'center'}),
    html.P([html.Sup(f'{total_releases}', style={'font-size': '1.7em', 'margin-top': '-0.5em','font-weight':'500', 'font-family': 'sans-serif', 'color': '#2ad9a8'}),        html.Br(),        html.Span('Total pgSIT Released', style={'font-size': '1.0em'})    ], style={'text-align': 'center'})
]
    return children


import webbrowser

#url = 'http://127.0.0.1:8050/'
#webbrowser.open_new(url)



if __name__ == '__main__':
    app.run_server(debug=True)


