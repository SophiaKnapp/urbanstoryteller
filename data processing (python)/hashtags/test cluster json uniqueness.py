
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


min_count = 17
res = '1.8'

path = os.path.join(GREEDY_MODULARITY_DIR, 'min_count_' + str(min_count) + '_res_' + res)


for quarter in POTATOES_LIST():
    path_quarter = os.path.join(path, quarter)
    files_quarter = sorted(glob(path_quarter + '/*_.csv'))    
    data = []

    df_uniqueness = load_dataframe(HASHTAG_TOP_DIR, quarter)
    df_uniqueness['hashtag'] = df_uniqueness['hashtag'].astype(str)
    
    for file in files_quarter:
        df = pd.read_csv(file)
        print(df[:5])

        df['hashtag'] = df['hashtag'].astype(str)
        df = df.merge(df_uniqueness[['hashtag', 'opacitysigmoidlog']], how='left', on='hashtag')

        df['opacity'] = np.round(df['opacitysigmoidlog'], decimals=2)

        df = df[['hashtag', 'count', 'opacity']]

        name = df.iloc[0].hashtag
        df.rename(columns={'hashtag': 'name'}, inplace=True)
        records = df.to_dict('records')
        data.append({'name':name, 'children': records})

    final_data = {"name": quarter, "children": data}

    out_path = os.path.join(CLUSTERS_DIR_JSON, quarter + '.json')
    with open(out_path, "w") as outfile:
        json.dump(final_data, outfile)