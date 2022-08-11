# Environment used: dash1_8_0_env
import sys
import math

sys.path.append('..')
import pandas as pd     #(version 1.0.0)
import geopandas as gpd

# print(px.data.gapminder()[:15])
from utils.utils import load_dataframe, read_result_csv
from utils.paths import HASHTAG_FREQUENCY_DIR_JSON, CLUSTERS_DIR, HASHTAG_FREQUENCY_DIR_ALL, POST_COUNT_DIR_JSON, HASHTAG_FREQUENCY_DIR, HASHTAGS_PER_USER_DIR, POTATOES_DIR, POTATOES_LIST, make_dir, POTATOES_CLEANED_DIR, GREEDY_MODULARITY_SELECTED_DIR, HASHTAG_TOP_DIR, make_dirs

import json
import os
from glob import glob

df_post_count = load_dataframe(POTATOES_DIR, 'post_counts')
# gdf = gpd.read_file('test.json')

# gdf['avg_x'] = gdf['geometry'].apply(lambda row: row.centroid.x)
# gdf['avg_y'] = gdf['geometry'].apply(lambda row: row.centroid.y)


# def get_markers():
#     quarter_markers_gdf = gpd.GeoDataFrame(gdf.copy(), geometry=gpd.points_from_xy(gdf.avg_x, gdf.avg_y))
#     quarter_markers_gdf = quarter_markers_gdf.merge(df_post_count, how='left', left_on='id', right_on='quarter')

#     # print(quarter_markers_gdf[:10])

#     result =  quarter_markers_gdf[['id', 'geometry']]
#     result.set_index('id', inplace=True)
#     print(result[:10])
#     with open('centers.json', 'w') as f:
#         f.write(result.to_json())


def csv_to_json(fromDir, toDir, quarter):
    # df = load_dataframe(HASHTAG_FREQUENCY_DIR, "allach")

    df = pd.read_csv(os.path.join(fromDir, quarter + ".csv"), index_col=0)
    print(len(df))
    df.drop(df[df['count'] < 5].index, inplace = True)
    print(len(df))

    # df.set_index('')
    result = df.to_json()

    # result.set_index()

    with open(os.path.join(toDir, quarter + '.json'), 'w') as f:
        f.write(result)

def frequencies_to_json():
    for potato in POTATOES_LIST():
        csv_to_json(HASHTAG_FREQUENCY_DIR, HASHTAG_FREQUENCY_DIR_JSON, potato)


# PER DISTRICT
def posts_to_json():
    dir = POTATOES_CLEANED_DIR
    for quarter in POTATOES_LIST():
        path = os.path.join(dir, quarter + ".csv")
        print(path)
        df = pd.read_csv(path, index_col=0) 
        df.reset_index(drop=True, inplace=True)
        if (df['is_video'].dtype != bool) :
            df.replace({'is_video': {'True': True, 'False': False}}, inplace=True)

        df['is_video'] = df['is_video'].astype(bool)
        df = df[~df['is_video']]
        df = df.sort_values(by='likes', ascending=False)

        df.reset_index(drop=True, inplace=True)
        df = df[['post_url', 'hashtags', 'likes']]        
        result = df.to_json()
        new_dir = os.path.join(dir, 'json')
        make_dir(new_dir)

        with open(os.path.join(new_dir, quarter + '.json'), 'w') as f:
            f.write(result)


# CITY
def posts_to_json_city():
    dir = POTATOES_CLEANED_DIR

    df_all = pd.DataFrame(columns=['post_url', 'hashtags', 'likes', 'is_video'])
    for quarter in POTATOES_LIST():
        path = os.path.join(dir, quarter + ".csv")
        print(path)
        df = pd.read_csv(path, index_col=0) 
        df.reset_index(drop=True, inplace=True)
        if (df['is_video'].dtype != bool) :
            df.replace({'is_video': {'True': True, 'False': False}}, inplace=True)

        df['is_video'] = df['is_video'].astype(bool)
        df = df[~df['is_video']]
        df_all = df_all.append(df)
        print(len(df_all))
        print(df_all.columns)


    print(len(df))
    df = df.drop_duplicates(subset='post_url', keep="first")
    print(len(df))   
        
    # if (.dtype != bool) :
    #         df.replace({'is_video': {'True': True, 'False': False}}, inplace=True)
    df_all['likes'] = df_all['likes'].astype(int)
    df_all = df_all.sort_values(by='likes', ascending=False)
    df_all.reset_index(drop=True, inplace=True)
    df_all.drop(df_all[df_all['hashtags'] == '[]'].index, inplace = True)
    print(len(df_all))
    df_all.drop(df_all[df_all['likes'] < 100].index, inplace = True)
    print(len(df_all))

    df_all = df_all[['post_url', 'hashtags', 'likes']]    
    print(df_all[:10])    
    result = df_all.to_json()
    new_dir = os.path.join(dir, 'json')
    make_dir(new_dir)

    with open(os.path.join(new_dir, 'city.json'), 'w') as f:
        f.write(result)


def potato_list_count_users_stories():

    df_post_count = load_dataframe(POTATOES_DIR, 'post_counts')
    min_count = 10
    res = '1.8'

    df_post_count['stories'] = 0
    df_post_count['users'] = 0


    path_to_clusters = os.path.join(GREEDY_MODULARITY_SELECTED_DIR, 'min_count_' + str(min_count) + '_res_' + res)

    for quarter in POTATOES_LIST():
        path_quarter_clusters = os.path.join(path_to_clusters, quarter)
        files_quarter = sorted(glob(path_quarter_clusters + '/*_.csv'))

        stories_count = len(files_quarter)
        df_users = load_dataframe(HASHTAGS_PER_USER_DIR, quarter)
    
        users_count = len(df_users.hashtags)
        print(users_count)

        index = df_post_count.loc[df_post_count['quarter'] == quarter].index

        df_post_count['stories'][index] = stories_count
        df_post_count['users'][index] = users_count
        
        

    df_post_count['post_count'] = df_post_count['post_count_cleaned']
    print(df_post_count)

    df_post_count = df_post_count[['quarter','post_count','users', 'stories']]

    df_post_count.to_json(os.path.join(POST_COUNT_DIR_JSON, 'posts_users_stories.json'), orient='records')


def checkRow(x, hashtags):
    if x in hashtags:
        return True
    else:
        return False

def count_all_quarters_to_json():
    df = load_dataframe(HASHTAG_FREQUENCY_DIR_ALL, 'count_all_quarters')
    print(len(df))
    df.drop(df[df['count'] <100].index, inplace = True)
    print(len(df))

    potatoes = POTATOES_LIST()

    # mask = (df['hashtag'].apply(lambda x: checkRow(x, potatoes)))
            # print(mask)
            # df['cluster'][mask] = name

    df.drop(df[df['hashtag'].apply(lambda x: checkRow(x, potatoes))].index, inplace = True)
    print(len(df))
     
    # df = df.sort_values(by='hashtag')

    
    df = df[['hashtag']]
    # df = df.set_index('hashtag')
    
    print(df)

    df.to_json(os.path.join(POST_COUNT_DIR_JSON, 'top_hashtags_city.json'))

    df = df.sort_values(by='hashtag')
    df.to_json(os.path.join(POST_COUNT_DIR_JSON, 'top_hashtags_city_sorted.json'))


# count_all_quarters_to_json()

make_dirs()
frequencies_to_json()