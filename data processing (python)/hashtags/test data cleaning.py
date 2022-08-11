import sys 
sys.path.append('..')
from utils.paths import make_dirs, QUARTERS_DICT, POTATOES_CLEANED_DIR, SEARCH_HASHTAGS_LIST, FORBIDDEN_HASHTAGS_LIST, POTATOES_HASHTAGS_CLEAN, QUARTER_RESULTS, POTATOES_DIR, QUARTERS_ALL_POSTS, HASHTAGS_PER_USER_DIR, HASHTAG_FREQUENCY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR
from utils.utils import load_dataframes, load_dataframe, write_dict_to_csv, write_list_to_csv, write_df_to_csv
import pandas as pd
import os


def checkRow(rowHashtags, hashtags):
    if len(set.intersection(set(rowHashtags), set(hashtags))) > 0:
        return True
    else:
        return False

make_dirs()


df_hashtags_clean = POTATOES_HASHTAGS_CLEAN()

selected_columns = ['owner_id','shortcode','hashtags', 'caption', 'post_url']

df_post_counts = pd.DataFrame(columns=['quarter', 'post_count', 'post_count_cleaned'])

forbidden_hashtags = set(FORBIDDEN_HASHTAGS_LIST())
search_hashtags = SEARCH_HASHTAGS_LIST()

for index, row in df_hashtags_clean.iterrows():
    # merge files if different hashtags are used
    print('>> now processing', row.POTATOES)
    if len(row.HASHTAG)>0:
        df = pd.DataFrame()
        for hashtag in row.HASHTAG:
            df_new = QUARTER_RESULTS(hashtag)
            df_new_hashtags = df_new[selected_columns]
            df = df.append(df_new_hashtags,ignore_index=True)
    else:
        df = QUARTER_RESULTS(row.POTATOES)
        df =df[selected_columns]
    
    # clean irrelevant posts
    post_count = len(df)
    if (len(row.CLEAN)>0):
        # df["to_clean"] = df.apply(lambda df_row: len(set.intersection(set(df_row.hashtags), set(row.CLEAN))), axis=1)
        # df.drop(df[df['to_clean'] != 0].index, inplace = True)

        mask = (df['hashtags'].apply(lambda x: checkRow(x, search_hashtags)))
        df = df[mask]

        
    post_count_cleaned = len(df)
    new_row = {'quarter': row.POTATOES, 'post_count': post_count, 'post_count_cleaned': post_count_cleaned}
    df_post_counts = df_post_counts.append(new_row, ignore_index=True)

    # clean forbidden hashtags
    df['hashtags'] = df['hashtags'].apply(lambda x: sorted(set(x).difference(forbidden_hashtags)))

    # write files
    write_df_to_csv(df, row.POTATOES, POTATOES_CLEANED_DIR)
    print(df_post_counts)
    
write_df_to_csv(df_post_counts, 'post_counts', POTATOES_DIR)