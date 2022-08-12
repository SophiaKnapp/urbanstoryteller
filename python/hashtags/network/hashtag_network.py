import sys
sys.path.append('..')
import pandas as pd
import os
from glob import glob
from utils.utils import get_literals
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def count_hashtag_network(df, df_frequency, n_nodes, out_csv, one_vote_per_user):
    df = df[['owner_id', 'shortcode', 'hashtags']]
    most_common_hashtags = list(df_frequency[:n_nodes]['hashtag'])
    df['hashtags'] = df['hashtags'].apply(lambda x: clean_irrelevant_hashtags(x, most_common_hashtags))

    # if one_vote_per_user:
    #   df = df.groupby('owner_id').agg(
    #     hashtags=pd.NamedAgg(column='hashtags', aggfunc='sum'), 
    #     post_count=pd.NamedAgg(column='shortcode', aggfunc='count')
    #   )
    #   df = df.sort_values(by=['post_count'], ascending=False)
    #   df['hashtags'] = df['hashtags'].map(lambda x: list(set(x)))

    edges = []

    for row in df.itertuples():
      hashtags_row = row.hashtags
      for index, hashtag in enumerate(hashtags_row):
        i = index +1
        while i < len(hashtags_row):
          other_hashtag = hashtags_row[i]
          if hashtag != other_hashtag:
            if hashtag < other_hashtag:
              edges.append((hashtag, other_hashtag))
            else:
              edges.append((other_hashtag, hashtag))
          i = i+1
  
    df_edges = pd.DataFrame(edges, columns=['source','target'])
    df_edges = df_edges.groupby(['source', 'target']).size().reset_index().rename(columns={0:'count'})
    df_edges = df_edges.sort_values(by=['count'], ascending=False)
    print(df_edges[:30])
    df_edges.to_csv(out_csv)

def generate_network_graph(df, n_nodes, out_file):
    G = nx.from_pandas_edgelist(df[:n_nodes], create_using=nx.Graph(), edge_attr=True)
    # plt.figure(3, figsize=(n_nodes,50)) 
    nx.draw(G, node_color="skyblue", node_size=500, with_labels=True, font_size=5, width=0.2)
    plt.savefig(out_file, dpi=300)
    plt.clf()

def generate_network_graph_rank(df_network, df_rank, n_nodes, out_file):
    top_tags = list(df_rank[:n_nodes]['hashtag'])
    # df_network.drop(df_network[not (df_network['source'] in top_tags)].index, inplace = True)
    print(len(df_network))
    df_network = df_network[~df_network['source'].isin(top_tags)]
    print(len(df_network))
    df_network = df_network[~df_network['target'].isin(top_tags)]
    print(len(df_network))



    G = nx.from_pandas_edgelist(df_network[:n_nodes], create_using=nx.Graph(), edge_attr=True)
    # plt.figure(3, figsize=(n_nodes,50)) 
    nx.draw(G, node_color="skyblue", node_size=400, with_labels=True, font_size=3, width=0.2)
    plt.savefig(out_file, dpi=300)
    plt.clf()

  
def clean_irrelevant_hashtags(hashtags, selected_hashtags):
  new_list = [hashtag for hashtag in hashtags if hashtag in selected_hashtags]
  return new_list
