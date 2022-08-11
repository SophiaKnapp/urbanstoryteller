from glob import glob
import sys
sys.path.append('..')
from utils.utils import read_result_csv, get_literals, get_list
import pandas as pd
import os

PATHS_TO_QUARTERS_FOLDER = '../../data/Instagram-API/Feed/Actors/hashtag-'
PATH_TO_RESULT = '/result/result.csv'
PATHS_TO_QUARTERS = sorted(glob('../../data/Instagram-API/Feed/Actors/hashtag-*/result/result.csv'))
PATHS_TO_PUBLIC_SPACES = sorted(glob('../../data/Instagram-API/Feed/Actors/PublicSpaces-hashtag-*/result/result.csv'))
HASHTAGS_PER_USER_DIR = '../../data/processed/hashtags_per_user'
HASHTAGS_PER_USER_PUBLIC_SPACES_DIR = '../../data/processed/publicSpaces/hashtags_per_user'
HASHTAG_FREQUENCY_DIR = '../../data/processed/hashtag_frequency'
HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR= '../../data/processed/publicSpaces/hashtag_frequency'
CONNECTED_COMPONENTS_DIR = '../../data/processed/hashtag_connected_components'
CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR = '../../data/processed/publicSpaces/hashtag_connected_components'
USERS_GRAPHS_DIR = '../../data/processed/user_graphs'
FREQUENT_ITEM_SETS_DIR = '../../data/processed/hashtag_frequent_item_sets'
GREEDY_MODULARITY_DIR = '../../data/processed/hashtag_greedy_modularity'
GREEDY_MODULARITY_SELECTED_DIR = '../../data/selected/hashtag_greedy_modularity'
CLUSTERS_DIR = '../../data/processed/clusters'
CSV_DIR = '../../data/csv'
POTATOES_HASHTAGS_CLEAN_PATH = os.path.join(CSV_DIR, 'potatoes_hashtags_hashtagstoclean.csv')
FORBDDEN_HASHTAGS_PATH = os.path.join(CSV_DIR, 'forbidden_hashtags.csv')
SEARCH_HASHTAGS_PATH = os.path.join(CSV_DIR, 'search_hashtags.csv')

HASHTAG_FREQUENCY_DIR_ALL = '../../data/processed/hashtag_frequency_all'
HASHTAG_TOP_FLOP_DIR = '../../data/processed/hashtags_topflop'
HASHTAG_TOP_DIR = '../../data/processed/hashtags_top'

HASHTAG_TOP_DIR_JSON = '../../data/json/hashtags_top'
CLUSTERS_DIR_JSON = '../../data/json/clusters'
POST_COUNT_DIR_JSON = '../../data/json'
HASHTAG_FREQUENCY_DIR_JSON = '../../data/hashtag_frequency'

POTATOES_DIR = '../../data/cleaned/potatoes'
POTATOES_CLEANED_DIR = '../../data/cleaned/potatoes/posts'

def POTATOES_LIST(n=-1):
    df = pd.read_csv(POTATOES_HASHTAGS_CLEAN_PATH)
    potatoes = df['POTATOES']
    potatoes = potatoes.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    if n < 0:
        n = len(potatoes)
    return list(potatoes)[:n]

def FORBIDDEN_HASHTAGS_LIST():
    df = pd.read_csv(FORBDDEN_HASHTAGS_PATH)
    hashtags = df['HASHTAGS']
    hashtags = hashtags.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    return list(hashtags)

def SEARCH_HASHTAGS_LIST():
    df = pd.read_csv(SEARCH_HASHTAGS_PATH)
    hashtags = df['HASHTAGS']
    hashtags = hashtags.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    return list(hashtags)


def POTATOES_HASHTAGS_CLEAN(n = -1):
    df = pd.read_csv(POTATOES_HASHTAGS_CLEAN_PATH)
    if (n>0):
        df = df[:n]
    df['POTATOES'] = df['POTATOES'].map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    df['HASHTAG'] = df['HASHTAG'].apply(lambda x: get_list(x))
    df['CLEAN'] = df['CLEAN'].apply(lambda x: get_list(x))

    return df

def QUARTER_RESULTS(quarter):
    path = PATHS_TO_QUARTERS_FOLDER + quarter + PATH_TO_RESULT
    return read_result_csv(path)

def QUARTER_CLEANED_RESULTS(quarter):
    path = os.path.join(POTATOES_CLEANED_DIR, quarter + '.csv')
    return read_result_csv(path)

def QUARTERS_DICT(n=-1):
    potatoes = POTATOES_LIST()
    if n<0:
        n = len(potatoes)
    quarters = {}
    potatoes = potatoes[:n]
    # for path in PATHS_TO_QUARTERS[:n]:
    #     quarter_name = path.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    #     print ('>> now loading:', quarter_name)
    #     df = read_result_csv(path)
    #     quarters[quarter_name] = df
    for quarter in potatoes:
        print ('>> now loading:', quarter)
        quarters[quarter] = QUARTER_CLEANED_RESULTS(quarter)
    return quarters

def QUARTERS_ALL_POSTS(n=len(PATHS_TO_QUARTERS)):
    df = pd.DataFrame()
    idx = 1
    for path in PATHS_TO_QUARTERS[:n]:
        idx += 1
        quarter_name = path.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
        print ('>> now loading:', quarter_name)
        df_new = read_result_csv(path)
        df_new_hashtags = df_new[['owner_id','shortcode','hashtags']]
        df = df.append(df_new_hashtags,ignore_index=True)

    print(df[:10])
    print(len(df))
    df = df.drop_duplicates(subset=['shortcode'])
    print(len(df))
    return df

def PUBLIC_SPACES_DICT(n=len(PATHS_TO_PUBLIC_SPACES)):
    quarters = {}
    for path in PATHS_TO_PUBLIC_SPACES[:n]:
        quarter_name = path.replace('../../data/Instagram-API/Feed/Actors/PublicSpaces-hashtag-','').replace('/result/result.csv', '')
        print ('>> now loading:', quarter_name)
        df = read_result_csv(path)
        quarters[quarter_name] = df

    return quarters


def make_dirs():
  dirs = [HASHTAG_FREQUENCY_DIR_JSON, HASHTAGS_PER_USER_DIR, POST_COUNT_DIR_JSON, CLUSTERS_DIR_JSON, HASHTAG_TOP_DIR_JSON, HASHTAG_TOP_DIR, POTATOES_CLEANED_DIR, POTATOES_DIR, HASHTAG_FREQUENCY_DIR, GREEDY_MODULARITY_DIR, CONNECTED_COMPONENTS_DIR, CONNECTED_COMPONENTS_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_PUBLIC_SPACES_DIR, HASHTAGS_PER_USER_PUBLIC_SPACES_DIR, HASHTAG_FREQUENCY_DIR_ALL]
  for dir in dirs: 
    if not os.path.exists(dir):
        os.makedirs(dir)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

