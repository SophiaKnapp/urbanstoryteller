import sys

from sympy import true 
sys.path.append('..')
from utils.paths import POST_COUNT_DIR_JSON, make_dirs, POTATOES_LIST, CLUSTERS_DIR_JSON, QUARTERS_DICT, GREEDY_MODULARITY_DIR, HASHTAG_TOP_DIR_JSON, HASHTAG_TOP_DIR, HASHTAG_FREQUENCY_DIR_ALL, POTATOES_CLEANED_DIR, FORBIDDEN_HASHTAGS_LIST, POTATOES_HASHTAGS_CLEAN, QUARTER_RESULTS, POTATOES_DIR, QUARTERS_ALL_POSTS, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR
from utils.utils import load_dataframes, load_dataframe, write_dict_to_csv, write_list_to_csv, write_df_to_csv, read_result_csv
import pandas as pd
import os
import json

import math



make_dirs()


df = load_dataframe(POTATOES_DIR, 'post_count')
# df = df[['hashtag', 'count', 'opacitysigmoidlog']]
# highest_rank = max(df['rank'])
# df['rank'] = df['rank'] / highest_rank


# df.columns= ['text', 'count', 'opacity']
# df['opacity'] = np.round(df['opacity'], decimals=2)

# path = os.path.join(HASHTAG_TOP_DIR_JSON, quarter + '.json')
df.set_index('quarter', inplace=True)

test_dict = df.to_dict(orient='index')
print(test_dict)

test_dict2 = {}

for k in test_dict:
    test_dict2[k] = test_dict[k]['post_count']

print(test_dict2)


with open(POST_COUNT_DIR_JSON + '/post_count.json', "w") as outfile:
    json.dump(test_dict2, outfile)