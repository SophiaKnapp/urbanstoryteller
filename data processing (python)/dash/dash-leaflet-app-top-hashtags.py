# Environment used: dash1_8_0_env
import sys
from tokenize import String

sys.path.append('..')
import os
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
import geopandas as gpd
import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# print(px.data.gapminder()[:15])
from utils.utils import load_dataframe
from utils.paths import HASHTAG_FREQUENCY_DIR, POTATOES_DIR
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
from dash_extensions.javascript import arrow_function, assign, Namespace

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_post_count = load_dataframe(POTATOES_DIR, 'post_counts')
gdf = gpd.read_file('test.json')
max_post_count = max(list(df_post_count['post_count_cleaned']))
post_count_and_geometry = gdf.merge(df_post_count, how='left', left_on='id', right_on='quarter')
post_count_and_geometry['opacity'] = post_count_and_geometry['post_count_cleaned']/max_post_count
post_count_and_geometry['tooltip'] = post_count_and_geometry['id']
print(post_count_and_geometry[['id','opacity']])

# print(gdf)
# print(gdf[gdf['id']==0])

my_map_style = {'width': '100%', 'height': '500px'}

potato_style = dict(color="black", fillColor="green", fillOpacity=0.1, weight=0)
potato_hover_style = dict(color="green", fillColor="green", weight=2)

# classes = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
# colorscale = ['#6ca6ca','#6195b5','#5684a1','#4b748d','#406379','#365365','#2b4250','#20313c','#152128','#0a1014','#000000']

style_handler = Namespace('choropleth', 'default')('StyleHandler')


# --------------- CLUSTERS

# geojson = json.loads(statecities.to_json())
# geobuf = dlx.geojson_to_geobuf(geojson)

# #PLAN:
# # depending on selection: have clusters read from cluster file (only show them for one part?)
# # when not selected: different clusters
# cities = dl.GeoJSON(data=geobuf,
#     id="geojson",
#     format="geobuf",
#     options=dict(pointToLayer=point_to_layer),
#     cluster=True,
#     zoomToBoundsOnClick=True,
#     superClusterOptions=dict(radius=40, maxZoom=8, minPoints=5),
#     hideout=dict(colorProp=color_prop,
#         cirleOptions=dict(fillOpacity=1,
#             stroke=False,
#             radius=3
#         ),
#         min=0,
#         max=vmax,
#         colorscale=colorscale
#     )
# )

#---------------------------------------------------------------

potato_layer = dl.GeoJSON(
    data=json.loads(post_count_and_geometry.to_json()), 
    zoomToBoundsOnClick=True,
    options=dict(style=style_handler),
    hoverStyle=arrow_function(potato_hover_style),
    # hideout=dict(classes=classes,
    #     colorscale=colorscale,
    #     style=potato_style,
    #     colorProp='post_count_cleaned'),
    hideout=dict(
        style=potato_style
    ),
    id='geojson'
    )
# zoomToBounds=True -> zoom to what is in the data layer

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(title='munich', id='munich_btn'),
            html.Button(id='quarter_btn'),
        ]),
        dbc.Col(
            html.Div([
                dl.Map(
                [potato_layer, dl.TileLayer(url="https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png")],
                center=[48.1374, 11.5754],
                zoom=11,
                style=my_map_style),
                # html.Button("Click me!", id='btn')
            ])
        ),
        dbc.Col([
            html.H1(id='info_title'),
            html.H5(id='n_posts'),
            html.Div(id='top_hashtags')
        ])
    ])
])

@app.callback([Output('info_title', 'children'),  Output('quarter_btn', 'title'), Output('n_posts', 'children'), Output('top_hashtags', 'children')], Input('geojson', 'click_feature'))
def update_output(click_data):
    if click_data is None:
        print("no data")
        raise PreventUpdate
    else:
        print(click_data)
        quarter = click_data['properties']['id']
        n_posts = str(click_data['properties']['post_count_cleaned']) + ' posts'
        df_top_hashtags = load_dataframe(HASHTAG_FREQUENCY_DIR, quarter)
        # print(list(df_top_hashtags['hashtag'][:10]))
        # print(click_data)

        top_hashtags = ' '.join('#'+ element for element in list(df_top_hashtags['hashtag'][:15]))
        print(top_hashtags)

        return quarter, '/'+ quarter, n_posts, top_hashtags
    # if n_clicks and (n_clicks % 2 ==1):
    #     return json.loads(post_count_and_geometry[post_count_and_geometry.id==0].to_json())
    # else:
    #     return json.loads(post_count_and_geometry.to_json())


# app.layout = html.Div([

#     html.Div([
#         dcc.Graph(id='the_graph')
#     ]),

#     # I should do: type='text' https://dash.plotly.com/dash-core-components/input

#     html.Div([
#         dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007,
#                   max=2007, min=1952, step=5, required=True),
#         # dcc.Input(id='selected_hashtag', type='text', value='hashtag'),
#         html.Button(id='submit_button', n_clicks=0, children='Submit'),
#         html.Div(id='output_state'),
#     ],style={'text-align': 'center'}),

# ])

# #---------------------------------------------------------------
# @app.callback(
#     [Output('output_state', 'children'),
#     Output(component_id='the_graph', component_property='figure')],
#     [Input(component_id='submit_button', component_property='n_clicks')],
#     [State(component_id='input_state', component_property='value')]
# )
# # if I change state to input: callback gets called every time I change it, not just when I click the button

# # number of inputs and outputs like callback
# def update_output(num_clicks, val_selected):
#     if val_selected is None:
#         raise PreventUpdate
#     else:
#         # data by plotly: px.data.gapminder()
#         # df = px.data.gapminder().query("year=={}".format(val_selected)) # filtering the data
#         # print(df[:3])

#         data={'id':['Karan','Rohit','Sahil','Aryan'],'Age':[23,22,21,24]}

#         df=pd.dataframe(data)
#         df = pd.DataFrame

#         fig = px.choropleth(df, locations="iso_alpha",
#                             color="lifeExp",
#                             hover_name="country",
#                             projection='natural earth',
#                             title='Munich',
#                             color_continuous_scale=px.colors.sequential.Plasma)

#         fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
#                           margin=dict(l=60, r=60, t=50, b=50))

#         return ('The input value was "{}" and the button has been \
#                 clicked {} times'.format(val_selected, num_clicks), fig)

if __name__ == '__main__':
    app.run_server(debug=True)