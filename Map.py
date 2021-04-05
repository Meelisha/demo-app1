import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# import gunicorn

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("Interactive Map_filter_violation2.csv")
viola = pd.read_csv("Violation only.csv")
vio_data = viola["Violation_Type"]
option_vio=[{"label":i,"value":i} for i in vio_data]


#df = df.groupby(['Year', 'Quarter', 'Violation', 'Is Health Based'])[["PWS ID"]].sum()
#df.reset_index(inplace=True)


# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([

    html.H1("Violation Data of Community Water System", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2014", "value": 2014},
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019}],

                 multi=False,
                 value=2014,
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="slct_quarter",
                 options=[
                     {"label": "Q1", "value": "Q1"},
                     {"label": "Q2", "value": "Q2"},
                     {"label": "Q3", "value": "Q3"},
                     {"label": "Q4", "value": "Q4"}],
                 multi=False,
                 value="Q1",
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="slct_violation",
                 options=option_vio,
                 multi=False,
                 value=vio_data[1],
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="slct_health",
                 options=[
                     {"label": "Y", "value": "Y"},
                     {"label": "N", "value": "N"},],
                 multi=False,
                 value="Y",
                 style={'width': "40%"}
                 ),


    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='violation_map', figure={}),
    dcc.Graph(id='table', figure={})

])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='violation_map', component_property='figure'),
     Output(component_id='table', component_property='figure')],

    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_quarter', component_property='value'),
     Input(component_id="slct_violation", component_property='value'),
     Input(component_id='slct_health', component_property='value')]
)
def update_graph(year,quarter,violation,health):

    container = "The year chosen by user was: {}".format(year)

    dff = df.copy()
    dff = dff[dff["Year"] == year]
    dff = dff[dff["Quarter"] == quarter]
    dff = dff[dff["Violation_Type"] == violation]
    dff = dff[dff["Is_Health_Based"] == health]


    # fig = px.scatter_mapbox(
    #       dff,
    #       lat="LATITUDE",
    #       lon="LONGITUDE",
    #       hover_name=("PWS_ID","Population_Served"),
    #
    #       color_discrete_sequence=["fuchsia"],
    #
    #        )
    #
    # fig.update_layout(mapbox_style="open-street-map")

    fig = go.Figure(go.Scattermapbox(
        text=dff.PWS_ID,

        lat=dff.LATITUDE,
        lon=dff.LONGITUDE,
        mode="markers",
        marker = go.scattermapbox.Marker(
        size=15
        ),


    hovertemplate=
        "<b>PWS ID:%{text}</b><br>"+
        "Population Served: %{dff.Population_Served}<br>"+
        "Site name:%{dff.Site_name}"




    ))

    fig.update_layout(mapbox_style="open-street-map",
                      autosize=True,
                      hovermode='closest',
                      mapbox=dict(bearing=0,
                                  center=dict(lat=42.5,lon=-72.5),
                          zoom=8,pitch=0),)





    # fig.update_layout(
    #     mapbox_style="white-bg",
    #     mapbox_layers=[
    #         {
    #             "below": 'traces',
    #             "sourcetype": "raster",
    #             "sourceattribution": "United States Geological Survey",
    #             "source": [
    #                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #             ]
    #         }
    #     ])
    fig.update_layout(margin={"r": 0, "t": 1, "l": 0, "b": 0})
    #fig.show()
    fig2 = go.Figure(data=[go.Table(header=dict(values=list(dff.columns)[:8],fill_color='paleturquoise',align="left"),
                                   cells=dict(values=[dff.Source_Name, dff.Organization, dff.Year,dff.Quarter,dff.PWS_ID,dff.Violation_Type,dff.Violation_Category_Code,dff.Is_Health_Based],
                                    fill_color='lavender',
                                    align="left"))

                          ])






    return container,fig,fig2   #return the number of outputs, in this case its 2: children and figure

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
