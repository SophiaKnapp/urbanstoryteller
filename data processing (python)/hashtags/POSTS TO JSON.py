import sys 
sys.path.append('..')
from utils.paths import SEARCH_HASHTAGS_LIST, make_dirs, POTATOES_LIST, CLUSTERS_DIR_JSON, QUARTERS_DICT, GREEDY_MODULARITY_DIR, HASHTAG_TOP_DIR_JSON, HASHTAG_TOP_DIR, HASHTAG_FREQUENCY_DIR_ALL, POTATOES_CLEANED_DIR, FORBIDDEN_HASHTAGS_LIST, POTATOES_HASHTAGS_CLEAN, QUARTER_RESULTS, POTATOES_DIR, QUARTERS_ALL_POSTS, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR
from utils.utils import load_dataframes, load_dataframe, write_dict_to_csv, write_list_to_csv, write_df_to_csv
import pandas as pd
import os
from glob import glob
import json
import numpy as np

make_dirs()


def checkRow(rowHashtags, hashtags):
    if len(set.intersection(set(rowHashtags), set(hashtags))) > 0:
        return True
    else:
        return False
    
    # df = dfs[quarter]
# df = load_dataframe(HASHTAG_TOP_DIR, 'westend')
# print(', '.join(list(df['hashtag'])))


# df = QUARTER_RESULTS('westend')
# df_new = df[df['hashtag'].apply()]

hashtags = SEARCH_HASHTAGS_LIST()
selected_columns = ['owner_id','shortcode','hashtags', 'caption', 'post_url']

df = QUARTER_RESULTS('westend')
df = df[selected_columns]
print(len(df))
mask = (df['hashtags'].apply(lambda x: checkRow(x, hashtags)))
# print(mask)

# print(df[:10])
df = df[mask]
print(len(df))
print(df[:10])

