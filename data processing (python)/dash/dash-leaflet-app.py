# Environment used: dash1_8_0_env
from imp import init_builtin
import sys
import math

from sympy import Q
sys.path.append('..')
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
import geopandas as gpd
import dash             #(version 1.8.0)
from dash import ctx
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# print(px.data.gapminder()[:15])
from utils.utils import load_dataframe
from utils.paths import CLUSTERS_DIR, HASHTAG_FREQUENCY_DIR, POTATOES_DIR
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
from dash_extensions.javascript import arrow_function, assign, Namespace
import plotly.graph_objs as go
from plotly.offline import plot
import random
from wordcloud import WordCloud
from shapely.geometry import Point, Polygon, mapping



# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# https://bootswatch.com/lux/
# app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app = dash.Dash()

initial_map_center = [48.1374, 11.5754]
initial_map_zoom = 13
initial_title = 'Munich'

df_post_count = load_dataframe(POTATOES_DIR, 'post_counts')
gdf = gpd.read_file('test.json')

gdf['avg_x'] = gdf['geometry'].apply(lambda row: row.centroid.x)
gdf['avg_y'] = gdf['geometry'].apply(lambda row: row.centroid.y)


dd_options = list(load_dataframe(HASHTAG_FREQUENCY_DIR, 'neuperlach')['hashtag'][:100])
print(dd_options)

def get_potatoes_and_opacity(quarter=None):
    post_count_and_geometry = gdf.copy().merge(df_post_count, how='left', left_on='id', right_on='quarter')
    max_post_count = max(list(df_post_count['post_count_cleaned']))
    post_count_and_geometry['opacity'] = post_count_and_geometry['post_count_cleaned']/max_post_count
    if quarter is None:
        return json.loads(post_count_and_geometry.to_json())
    else:
        quarter_selected = post_count_and_geometry.loc[post_count_and_geometry['id'] == quarter]
        return json.loads(quarter_selected.to_json())

def get_markers():
    quarter_markers_gdf = gpd.GeoDataFrame(gdf.copy(), geometry=gpd.points_from_xy(gdf.avg_x, gdf.avg_y))
    quarter_markers_gdf = quarter_markers_gdf.merge(df_post_count, how='left', left_on='id', right_on='quarter')


    quarters_geojson_data = dlx.geojson_to_geobuf(json.loads(quarter_markers_gdf.to_json()))
    return quarters_geojson_data

def coord_lister(geom):
    coords = list(geom.exterior.coords)
    return (coords)

def get_cluster_markers(quarter):
    number = 5
    quarter_selected = gdf.copy().loc[gdf['id'] == quarter]
    p = list(quarter_selected['geometry'].apply(coord_lister))[0]
    polygon = Polygon(p)


    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

        if polygon.contains(pnt):
            points.append(pnt)

    
    data_df = gpd.GeoDataFrame(geometry=points)

    data_df['id'] = ['architecture', 'food', 'gym', 'pep', 'ostpark']
    data_df['size'] = [1, 0.2, 0.8, 0.5, 0.75]
    data_json = data_df.to_json()


    data = dlx.geojson_to_geobuf(json.loads(data_json))
    return data


# get_markers()
# get_cluster_markers('neuperlach')



def get_tag_cloud(quarter=None):
    n = 30
    # word_cloud
    # words = []
    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(n)]

    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )

    words = dir(go)[:n]
    if quarter is not None:
        df_top_hashtags = load_dataframe(HASHTAG_FREQUENCY_DIR, quarter)
        words = list(df_top_hashtags['hashtag'][1:n+1])
        counts = list(df_top_hashtags['count'][1:n+1])
        top_count = max(list(counts))
        max_font_size = 30
        weights = [c/top_count*max_font_size for c in counts]
        data = go.Scatter(x=[random.random() for i in range(n)],
                        y=[random.random() for i in range(n)],
                        mode='text',
                        text=words,
                        marker={'opacity': 0.3},
                        textfont={'size': weights,
                                'color': colors})

        fig = go.Figure(data=[data], layout=layout)

        fig.update_layout(
            showlegend=False,
            height=500,
            margin=dict(l=10, r=10, t=10, b=20),
        )
        return fig

    else:
        fig = go.Figure(data=[], layout=layout)
        return fig


# def get_bar_chart(quarter=None):
#     n = 30
#     # word_cloud
#     # words = []

#     layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
#                         'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}},
#                         paper_bgcolor='rgba(0,0,0,0)',
#                         plot_bgcolor='rgba(0,0,0,0)'
#                         )

#     if quarter is not None:
        
#         d = {'col1': [1, 2], 'col2': [3, 4]}
#         df = pd.DataFrame(data=d)
#         fig = px.bar(df, x='col1', y='col2')

#         fig.update_layout(
#             showlegend=False,
#             height=200,
#             margin=dict(l=10, r=10, t=10, b=20),
#         )
#         return fig

#     else:
#         # fig = go.Figure(data=[], layout=layout)
#         return None

    


df_links = load_dataframe(CLUSTERS_DIR, 'neuperlach/beton')
df_links_2 = load_dataframe(CLUSTERS_DIR, 'neuperlach/natur')

links = list(df_links['post_url'][:12])

instagram_posts = [
    dbc.Col(
        html.Div(
            html.Iframe(
                src = link + 'embed/captioned/', 
                # height = '1000', 
                style = {'width':"200%", 'height':"200%", "border":'none', 'overflow-x':"scroll"}
                ), 
        
        style = {"transform": "scale(0.5)","transform-origin": "0 0"}
        ),
        width=1,
    )
    for link in links]

        # dbc.Col(html.Iframe(src = link + 'embed/captioned/', height = '500', style = {'width':"100%", 'height':"100%", "border":'none', 'overflow-x':"scroll"}) for link in links


# html.Iframe(src = str(URL + '/embed')  ),

my_map_style = {'width': '100%', 'height': '500px'}

potato_style = dict(color="black", fillColor="green", fillOpacity=0.1, weight=0)
potato_hover_style = dict(color="green", fillColor="green", weight=2)

# classes = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
# colorscale = ['#6ca6ca','#6195b5','#5684a1','#4b748d','#406379','#365365','#2b4250','#20313c','#152128','#0a1014','#000000']

style_handler = Namespace('choropleth', 'default')('StyleHandler')
point_to_layer = Namespace('choropleth', 'default')('PointToLayer')
point_to_layer_clusters = Namespace('choropleth', 'default')('PointToLayerClusters')


# plot(fig)


# --------------- CLUSTERS

# geojson = json.loads(statecities.to_json())
# geobuf = dlx.geojson_to_geobuf(geojson)

# #PLAN:
# # depending on selection: have clusters read from cluster file (only show them for one part?)
# # when not selected: different clusters
# cities = dl.GeoJSON(data=geobuf,
#     id="geojson
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

map_layer = dl.TileLayer(url="https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png")

# op= get_potatoes_and_opacity()
potato_layer = dl.GeoJSON(
    data=get_potatoes_and_opacity(),
    options=dict(style=style_handler),
    hoverStyle=arrow_function(potato_hover_style),
    zoomToBounds=True,
    hideout=dict(
        style=potato_style
    ),
    id='potatoes_geojson'
)



markers_layer = dl.GeoJSON(
                    data=get_markers(),
                    id='markers_geojson',
                    format='geobuf',
                    options=dict(pointToLayer=point_to_layer)
                )


clusters_layer = dl.GeoJSON(
                    data=None,
                    id='clusters_geojson',
                    format='geobuf',
                    options=dict(pointToLayer=point_to_layer_clusters)
                )

            

# quarter_selected = quarter_markers_gdf.loc[quarter_markers_gdf['id'] == 'altstadt']
# sel_test = dlx.geojson_to_geobuf(json.loads(quarter_selected.to_json()))

# clusters_geojson_data = dlx.geojson_to_geobuf(json.loads(cluster_markers_gdf.to_json()))
# charts = [dl.Minichart(lat=initial_map_center[0], lon=initial_map_center[1], type="pie", id="pie")]




app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            [
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(id="dropdown", value=[], options=dd_options, clearable=False, multi=True),
                    )
                ),
                html.Div(
                    dl.Map(
                        # [markers_layer, clusters_layer, potato_layer, map_layer],
                        [markers_layer, clusters_layer, potato_layer],

                        center=[48.1374, 11.5754],
                        zoom=11,
                        style=my_map_style,
                        id='map'
                    ),
                    id='map_div'
                ),
            ],
            width=6
        ),
         dbc.Col([
            html.H1(initial_title, id='title_label'),
            html.H5(id='n_posts'),
            dcc.Graph(figure=get_tag_cloud(), id='tag_cloud'),
            # dcc.Graph(id="bar_chart"),
        ],  width=6
        )
    ]),
    dbc.Row(
        children = instagram_posts, 
        id = 'instagram_posts'
    ),
    # dbc.Row([
    #     dbc.Col([
    #         html.H5(id='n_posts'),
    #         html.Div(id='top_hashtags')
    #     ])
    # ]),
    dcc.Store(id='selected_id_store', data=''),
])

# zoomed: no map, just info
# not zoomed: map, layer for each (always potato_)

@app.callback([
        Output('title_label', 'children'), 
        Output('n_posts', 'children'), 
        Output('potatoes_geojson', 'data'),
        Output('markers_geojson', 'data'),
        Output('clusters_geojson', 'data'),
        Output('tag_cloud', 'figure'),
        Output('selected_id_store', 'data'),
    ], 
    [
        Input('potatoes_geojson', 'click_feature'),
        Input('map', "click_lat_lng"),
        Input("dropdown", "value"),
        Input('selected_id_store', "data"),
    ]
)
def update_selected_quarter(click_data, map_click, dropdown_value, selected_id):
    print(dropdown_value)
    id_clicked = ctx.triggered_id
    if id_clicked == 'map':
        if map_click is None:
            raise PreventUpdate
        else:
            return [initial_title, '', get_potatoes_and_opacity(), get_markers() , None, get_tag_cloud(), dash.no_update]

    elif id_clicked == 'potatoes_geojson':
        if click_data is None:
            raise PreventUpdate
        else:
            print("IN THE UPDATE CLICKED {}".format(id_clicked))
            quarter = click_data['properties']['id']
            n_posts = str(click_data['properties']['post_count_cleaned']) + ' posts'
            
            # return initial_title + ' / '+ quarter, n_posts, top_hashtags, dash.no_update, dash.no_update, dash.no_update
        
            # quarter_selected_text = quarter_markers_gdf.loc[quarter_markers_gdf['id'] == quarter]
            # data = dlx.geojson_to_geobuf(json.loads(quarter_selected_text.to_json()))

            # print(quarters_geojson_data)
            return [initial_title +' / '+ quarter, n_posts, get_potatoes_and_opacity(quarter), None, get_cluster_markers(quarter), get_tag_cloud(quarter), quarter]

    # else:
        # return [initial_title, '', '', get_markers(), get_potatoes_and_opacity() , dash.no_update]

    # else: 
    #     if id_clicked == 'amount':
    #         return [dash.no_update, dash.no_update, dash.no_update, quarters_geojson_data, dash.no_update, 'amount']
    #     elif id_clicked == 'cluster':
    #         return [dash.no_update, dash.no_update, dash.no_update, clusters_geojson_data, dash.no_update, 'cluster']
    #         # return [clusters_geojson_data, 'cluster']
    #     elif id_clicked == 'type':
    #         return [dash.no_update, dash.no_update, dash.no_update, clusters_geojson_data, dash.no_update, 'type']

            # return [quarters_geojson_data, 'type']



# return title_label, n_posts, top_hashtags, markers_data, selected_id, mode
# Output('title_label', 'children'), 
#         Output('n_posts', 'children'), 
#         Output('top_hashtags', 'children'),
#         Output('markers_geojson', 'data'),
#         Output('selected_id_store', 'data'),
#         Output('mode_store', 'data')

# @app.callback(
#     [Output('markers_geojson', 'data'),
#     Output('mode_store', 'data')
#     ],
#     [
#         Input('amount', 'n_clicks'),
#         Input('cluster', 'n_clicks'),
#         Input('type', 'n_clicks'),
#     ])
# def update_mode(amount_clicks, cluster_clicks, type_clicks):
#     id_clicked = ctx.triggered_id
#     print(id_clicked)
#     if id_clicked == 'amount':
#         return [quarters_geojson_data, 'amount']
#     elif id_clicked == 'cluster':
#         return [clusters_geojson_data, 'cluster']
#     elif id_clicked == 'type':
#         return [quarters_geojson_data, 'type']


# @app.callback([Output('quarter_btn', 'children'), Output('n_posts', 'children'), Output('top_hashtags', 'children')], [Input('munich_btn','n_clicks'), Input('geojson', 'click_feature')])
# def update_mode(munich_clicks, click_data):
#     if click_data is None:
#         print("no data")
#         raise PreventUpdate
#     else:
#         if(munich_clicks is> 0):
#             print('>0')
#             return '', '', ''
#         else:
#             print("some data")
#             quarter = click_data['properties']['id']
#             n_posts = str(click_data['properties']['post_count_cleaned']) + ' posts'
#             df_top_hashtags = load_dataframe(HASHTAG_FREQUENCY_DIR, quarter)
#             top_hashtags = ' '.join('#'+ element for element in list(df_top_hashtags['hashtag'][:15]))
#             print(top_hashtags)

#         return '/  '+ quarter, n_posts, top_hashtags

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