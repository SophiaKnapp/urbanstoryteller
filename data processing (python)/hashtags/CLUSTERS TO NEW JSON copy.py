import sys

from sympy import true 
sys.path.append('..')
from utils.paths import make_dirs, POTATOES_LIST, CLUSTERS_DIR_JSON, QUARTERS_DICT, GREEDY_MODULARITY_SELECTED_DIR, HASHTAG_TOP_DIR_JSON, HASHTAG_TOP_DIR, HASHTAG_FREQUENCY_DIR_ALL, POTATOES_CLEANED_DIR, FORBIDDEN_HASHTAGS_LIST, POTATOES_HASHTAGS_CLEAN, QUARTER_RESULTS, POTATOES_DIR, QUARTERS_ALL_POSTS, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR
from utils.utils import load_dataframes, load_dataframe, write_dict_to_csv, write_list_to_csv, write_df_to_csv, read_result_csv
import pandas as pd
import os
from glob import glob
import json
import numpy as np
import math



make_dirs()


min_count = 10
res = '1.8'

def checkRow(x, hashtags):
    if x in hashtags:
        return True
    else:
        return False

path = os.path.join(GREEDY_MODULARITY_SELECTED_DIR, 'min_count_' + str(min_count) + '_res_' + res)

for quarter in POTATOES_LIST():
    path_quarter_clusters = os.path.join(path, quarter)
    path_quarter = os.path.join(HASHTAG_TOP_DIR, quarter + '_rank.csv')
    files_quarter = sorted(glob(path_quarter_clusters + '/*_.csv'))

    df = read_result_csv(path_quarter)
    df = df.drop(df['count_quarter'].idxmax())

    df['hashtag'] = df['hashtag'].astype(str)
    df['cluster'] = ""
    
    for file in files_quarter:
        df_cluster = pd.read_csv(file)
        hashtags = list(df_cluster['hashtag'])
        if len(hashtags) > 2:
            hashtags = hashtags[:15] # TODOO: check if that is good
            name = hashtags[0]
            mask = (df['hashtag'].apply(lambda x: checkRow(x, hashtags)))
            # print(mask)
            df['cluster'][mask] = name


    # df['opacity'] = np.round(df['opacitysigmoidlog'], decimals=2)


    top_count = np.max(df['count_quarter'])
    print(top_count)

    df['count'] = df['count_quarter']
    df['uniqueness'] = np.round(df['uniqueness'], decimals=2)


    
    df['radius'] = df['count']/math.pi
    df['radius'] = np.sqrt(df['radius'])
    df['radius'] = df['radius']/df['radius'].max()

    df['rank'] = df['count'] * df['uniqueness'] * df['uniqueness']

    df = df[['hashtag', 'count', 'radius', 'uniqueness', 'cluster', 'rank']]

    # final_data = {"name": quarter, "children": data}

    out_path = os.path.join(CLUSTERS_DIR_JSON, quarter + '.json')
    df.to_json(out_path, orient='records')
    # with open(out_path, "w") as outfile:
    #     json.dump(final_data, outfile)

