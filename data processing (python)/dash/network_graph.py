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
from utils.utils import load_dataframe, load_graph
from utils.paths import CLUSTERS_DIR, HASHTAG_FREQUENCY_DIR, POTATOES_DIR, GREEDY_MODULARITY_DIR
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
from dash_extensions.javascript import arrow_function, assign, Namespace
import plotly.graph_objs as go
from plotly.offline import plot
import random
from wordcloud import WordCloud
from shapely.geometry import Point, Polygon, mapping
import os
import networkx as nx



def get_network_graph(quarter=None):
    n = 30

    G = load_graph(os.path.join(GREEDY_MODULARITY_DIR, 'min_count_20_res_2.1', 'neuperlach'), 'architecture_architektur_urban_')
    pos = nx.shell_layout(G)


    weights = nx.get_edge_attributes(G, 'weight')
    counts = nx.get_node_attributes(G,'count')
    node_weights = nx.get_node_attributes(G,'weight')
    max_node_weight= max(node_weights.values())
    max_node_size = 50


    fig = go.Figure(
    # fig = go.Figure(data=[edge_trace],

             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )



    edge_traces=[]
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_traces.append(go.Scatter(
        x=[x0,x1], y=[y0,y1],
        line=dict(width=weights[edge], color='#888'),
        hoverinfo='none',
        mode='lines'))

    node_traces = []
    for node in G.nodes():
        x, y = pos[node]
        print(node)
        node_traces.append(go.Scatter(
            x=[x], y=[y],
            mode="text",
            hoverinfo='text',
            # textposition="top center",
            text=node,
            textfont_size=14,
            # marker_size=node_weights[node]/max_node_weight*max_node_size
        ))


        fig.add_shape(type="circle",
            line_color="blue", fillcolor="transparent",
            x0=0, y0=0, x1=2, y1=2
        )   


    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    # node_trace.marker.color = node_adjacencies
    # node_trace.text = node_text

    fig.add_traces(edge_traces)
    fig.add_traces(node_traces)
    


    fig.show()


    # data = go.Scatter(x=[random.random() for i in range(n)],
    #                 y=[random.random() for i in range(n)],
    #                 mode='text',
    #                 text=words,
    #                 marker={'opacity': 0.3},
    #                 textfont={'size': weights,
    #                         'color': colors})

    # fig = go.Figure(data=[data], layout=layout)

    # fig.update_layout(
    #     showlegend=False,
    #     height=500,
    #     margin=dict(l=10, r=10, t=10, b=20),
    # )
    # return fig

    # else:
    #     fig = go.Figure(data=[], layout=layout)
    #     return fig


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

    
if __name__ == '__main__':    
    # app.run_server(debug=True)
    get_network_graph()