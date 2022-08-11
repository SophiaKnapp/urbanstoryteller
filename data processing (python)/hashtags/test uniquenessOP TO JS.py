import sys 
sys.path.append('..')
from utils.paths import make_dirs, POTATOES_LIST, CLUSTERS_DIR_JSON, QUARTERS_DICT, GREEDY_MODULARITY_DIR, HASHTAG_TOP_DIR_JSON, HASHTAG_TOP_DIR, HASHTAG_FREQUENCY_DIR_ALL, POTATOES_CLEANED_DIR, FORBIDDEN_HASHTAGS_LIST, POTATOES_HASHTAGS_CLEAN, QUARTER_RESULTS, POTATOES_DIR, QUARTERS_ALL_POSTS, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR
from utils.utils import load_dataframes, load_dataframe, write_dict_to_csv, write_list_to_csv, write_df_to_csv
import pandas as pd
import os
from glob import glob
import json
import numpy as np

make_dirs()


for quarter in POTATOES_LIST():
    
    # df = dfs[quarter]
    df = load_dataframe(HASHTAG_TOP_DIR, quarter)
    df = df[['hashtag', 'count_quarter', 'opacitytanh']]
    # highest_rank = max(df['rank'])
    # df['rank'] = df['rank'] / highest_rank


    df.columns= ['text', 'count', 'opacity']
    df['opacity'] = np.round(df['opacity'], decimals=4)

    path = os.path.join(HASHTAG_TOP_DIR_JSON, quarter + '.json')
    df[:200].to_json(path, orient='records')