from re import A
import sys
sys.path.append('..')
from utils.paths import make_dirs, QUARTERS_DICT, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR
from utils.utils import load_dataframes
import pandas as pd
import os
from nltk.probability import FreqDist
import csv
import networkx as nx
from itertools import combinations
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure, text
import netgraph

# from networkx.drawing.nx_agraph import graphviz_layout


def generate_graph(df_frequencies, df_users, n_nodes, min_edge_weight, min_node_weight, min_degree, noise_treshold_1, noise_treshold_2, forbidden_hashtags=[]):

    df_frequencies_slice = df_frequencies[:n_nodes]
    df_frequencies_slice.drop(df_frequencies_slice[df_frequencies_slice['count'] < min_node_weight].index, inplace = True)

    # df_users= hashtags_per_user_dict[quarter]
    G = nx.Graph()
    most_common_hashtags = list(df_frequencies['hashtag'][:n_nodes])
    df_users['hashtags'] = df_users['hashtags'].apply(lambda x: [hashtag for hashtag in x if hashtag in most_common_hashtags and not hashtag in forbidden_hashtags])

    df_frequencies = df_frequencies[~ df_frequencies['hashtag'].isin(forbidden_hashtags)]

    for index, row in df_frequencies_slice.iterrows(): # does iterrows have arguments?
        G.add_node(row.hashtag, count=row['count'])
    
    for index, row in df_users.iterrows():
        pairs = res = list(combinations(row.hashtags, 2))
        for pair in pairs:
            if pair in G.edges:
                data = G.get_edge_data(pair[0], pair[1])
                G.add_edge(pair[0], pair[1], weight=data['weight']+1)
            else:
                G.add_edge(pair[0], pair[1], weight=1)

    for u, v in G.edges:
        count_A = G.nodes[u]['count']
        count_B = G.nodes[v]['count']
        edge_weight = G[u][v]['weight']

        if edge_weight < min_edge_weight:
            G.remove_edge(u, v)
        else: 

            per_A = edge_weight / count_A
            per_B = edge_weight / count_B

            if not (min(per_A,per_B) > noise_treshold_1/100):
                G.remove_edge(u, v)
            else:
                neighbors_A = [n for n in G.neighbors(u)]
                neighbors_B = [n for n in G.neighbors(v)]
                common_neighbors = [node for node in neighbors_A if node in neighbors_B]

                if not (min(len(common_neighbors)/len(neighbors_A), len(common_neighbors)/len(neighbors_B))) > noise_treshold_2/100:
                    G.remove_edge(u, v)

    remove = [node for node,degree in dict(G.degree()).items() if degree < min_degree]
    G.remove_nodes_from(remove)

    # max_node_size = 1000
    # max_font_size = 12

    # node_counts = list(nx.get_node_attributes(G, 'count') .values())
    # max_count = max(node_counts)
    # node_sizes = [count/max_count*max_node_size for count in node_counts]
    # # plt.figure(1, figsize=(10,10)) 

    # pos = nx.spring_layout(G)
    # nx.draw_networkx_nodes(G, pos, node_size=node_sizes, label=True)
    # nx.draw_networkx_edges(G, pos)
    # d = nx.get_node_attributes(G, 'count')
    # for node, (x, y) in pos.items():
    #     text(x, y, node, fontsize=d[node]/max_count*max_font_size, ha='center', va='center')

    # # plt.savefig(os.path.join(out_dir, name))


    # plt.clf()
    
    return G


def generate_graph_communities(df_frequencies, df_users, min_count, forbidden_hashtags=[]):

    df_frequencies.drop(df_frequencies[df_frequencies['count'] < min_count].index, inplace = True)
    # df_frequencies_slice.drop(df_frequencies_slice[df_frequencies_slice['count'] < min_node_weight].index, inplace = True)

    # df_users= hashtags_per_user_dict[quarter]
    G = nx.Graph()
    hashtags = [x for x in list(df_frequencies['hashtag']) if x not in forbidden_hashtags]
    # most_common_hashtags = hashtags[:n_nodes]
    df_users['hashtags'] = df_users['hashtags'].apply(lambda x: [hashtag for hashtag in x if hashtag in hashtags and not hashtag in forbidden_hashtags])

    df_frequencies = df_frequencies[~ df_frequencies['hashtag'].isin(forbidden_hashtags)]

    for index, row in df_frequencies.iterrows(): # does iterrows have arguments?
        G.add_node(row.hashtag, count=row['count'], weight=0) #remove count
    
    for index, row in df_users.iterrows():
        hashtags = row.hashtags
        pairs = list(combinations(hashtags, 2))

        if len(hashtags) > 0:
            node_weight = 1/len(hashtags) # for user: add fraction of weight to every hashtag-node
            for hashtag in hashtags:
                G.nodes[hashtag]['weight'] = G.nodes[hashtag]['weight'] + node_weight

            weight = 1/(len(hashtags))
            for pair in pairs:
                if pair in G.edges:
                    data = G.get_edge_data(pair[0], pair[1])
                    G.add_edge(pair[0], pair[1], weight=data['weight']+weight)
                else:
                    G.add_edge(pair[0], pair[1], weight=weight)
    return G


def generate_graph_communities_users(df_frequency, df, n_users, n_hashtags, forbidden_hashtags=[]):

    df = df[:n_users]
    G = nx.Graph()

    # print(df.columns)
    # df_slice = df_slice[~ df_slice['hashtag'].isin(forbidden_hashtags)]

    most_common_hashtags = list(df_frequency['hashtag'][:n_hashtags])


    df['hashtags'] = df['hashtags'].apply(lambda x: [hashtag for hashtag in x if hashtag in most_common_hashtags and not hashtag in forbidden_hashtags])
    # df_slice['hashtags'] = df_slice['hashtags'].apply(lambda x: [hashtag for hashtag in x if hashtag not in forbidden_hashtags])



    # Create nodes
    for index, row in df.iterrows(): # does iterrows have arguments?
        # G.add_node(row.owner_id, hashtags=row.hashtags)
        G.add_node(index, hashtags=row.hashtags)

    # for i in range(n_users):
    #     G.add_node(i, hashtags=row.hashtags)


    pairs = list(combinations(range(n_users),2))

    for u,v in pairs:
        hashtags_u = set(df.iloc[u].hashtags)
        hashtags_v = set(df.iloc[v].hashtags)
        shared_hashtags = set.intersection(hashtags_u,hashtags_v)

        # G.add_edge(row.owner_id, hashtags=row.hashtags, weight=len(shared_hashtags))
        if len(shared_hashtags) >= 1:
            # G.add_edge(df.iloc[u].owner_id, df.iloc[v].owner_id, weight=len(shared_hashtags), hashtags=shared_hashtags)
            # G.add_edge(df.iloc[u].owner_id, df.iloc[v].owner_id, weight=len(shared_hashtags))

            G.add_edge(u, v, weight=len(shared_hashtags), hashtags=shared_hashtags)


    # edge_counts = list(nx.get_edge_attributes(G, 'weight') .values())
    # print(edge_counts)

    # for u, v in G.edges:
    #     edge_weight = G[u][v]['weight']

    #     if edge_weight < min_edge_weight:
    #         G.remove_edge(u, v)

    # remove = [node for node,degree in dict(G.degree()).items() if degree < min_degree]
    # G.remove_nodes_from(remove)
    
    return G

def draw_graph(G, max_node_size, max_font_size, dpi, name, out_dir):
    node_counts = list(nx.get_node_attributes(G, 'count') .values())
    max_count = max(node_counts)

    node_sizes = [count/max_count*max_node_size for count in node_counts]

    edge_counts = list(nx.get_edge_attributes(G, 'weight') .values())
    
    if(len(edge_counts) >1):
        max_edge_count = max(edge_counts)
        edge_weights = [count/max_edge_count*2.0 for count in edge_counts]

        pos = nx.spring_layout(G, k=0.15, iterations=8)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#ADD8E6", label=True)
        nx.draw_networkx_edges(G, pos, width=edge_weights)
        d = nx.get_node_attributes(G, 'count')
        for node, (x, y) in pos.items():
            text(x, y, node, fontsize=d[node]/max_count*max_font_size, ha='center', va='center')

        plt.figure(1, figsize=(20,20)) 
        plt.savefig(os.path.join(out_dir, name), dpi=dpi)    
        plt.clf()


def draw_graph_users(G, max_font_size, name, out_dir):
    # node_counts = list(nx.get_node_attributes(G, 'count') .values())
    # max_count = max(node_counts)
    # node_sizes = [count/max_count*max_node_size for count in node_counts]

    edge_counts = list(nx.get_edge_attributes(G, 'weight') .values())
    
    if(len(edge_counts) >1):
        max_edge_count = max(edge_counts)
        edge_weights = [count/max_edge_count*2.0 for count in edge_counts]


        pos = nx.spring_layout(G, k=0.15, iterations=15)
        nx.draw_networkx_nodes(G, pos, node_color="#ADD8E6", label=True)
        # nx.draw_networkx_edges(G, pos, width=edge_weightse)
        nx.draw_networkx_edges(G, pos)

        # d = nx.get_node_attributes(G, 'count')
        # for node, (x, y) in pos.items():
        #     text(x, y, node, fontsize=d[node]/max_count*max_font_size, ha='center', va='center')

        # plt.figure(1, figsize=(20,20)) 
        plt.savefig(os.path.join(out_dir, name), dpi=1500)    
        plt.clf()



def draw_interactive_graph(G, max_node_size, max_font_size, name, out_dir):

    node_counts = list(nx.get_node_attributes(G, 'count') .values())
    max_count = max(node_counts)
    node_sizes = [count/max_count*max_node_size for count in node_counts]
    # plt.figure(1, figsize=(50,50)) 

    pos = nx.spring_layout(G)


    # decide on a layout

    # Create an interactive plot.
    # NOTE: you must retain a reference to the object instance!
    # Otherwise the whole thing will be garbage collected after the initial draw
    # and you won't be able to move the plot elements around.
    plot_instance = netgraph.InteractiveGraph(G, node_positions=pos)

    plot_instance.draw_nodes(G, pos, node_size=node_sizes, label=True)

    # netgraph.d

    ######## drag nodes around #########

    # To access the new node positions:
    node_positions = plot_instance.node_positions
        