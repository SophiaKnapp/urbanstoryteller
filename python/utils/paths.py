import sys
sys.path.append('..')
from utils.utils import read_result_csv, get_list
import pandas as pd
import os

PATHS_TO_QUARTERS = '../../data/raw'
HASHTAGS_PER_USER_DIR = '../../data/processed/hashtags_per_user'
HASHTAG_FREQUENCY_DIR = '../../data/processed/hashtag_frequency'
GREEDY_MODULARITY_DIR = '../../data/processed/hashtag_greedy_modularity'
GREEDY_MODULARITY_SELECTED_DIR = '../../data/selected/hashtag_greedy_modularity'
CSV_DIR = '../../data/csv'
POTATOES_HASHTAGS_AMBIGUOUS_PATH = os.path.join(CSV_DIR, 'potatoes_hashtags_ambiguous.csv')
MEANINGLESS_HASHTAGS_PATH = os.path.join(CSV_DIR, 'meaningless_hashtags.csv')
SEARCH_HASHTAGS_PATH = os.path.join(CSV_DIR, 'search_hashtags.csv')
HASHTAG_FREQUENCY_DIR_ALL = '../../data/processed/hashtag_frequency_all'
HASHTAG_TOP_DIR = '../../data/processed/hashtags_top'
CLEANED_DIR = '../../data/cleaned/potatoes'
POTATOES_CLEANED_DIR = '../../data/cleaned/potatoes/posts'
JSON_DIR_PUBLIC = '../../javascript/public/data'
JSON_DIR_ASSETS = '../../javascript/src/assets'
CLUSTERS_DIR_JSON = JSON_DIR_PUBLIC + '/clusters'
POSTS_DIR_JSON = JSON_DIR_PUBLIC + '/posts_json'

HASHTAG_FREQUENCY_DIR_JSON = JSON_DIR_ASSETS + '/hashtag_frequency_json'

def POTATOES_LIST(n=-1):
    df = pd.read_csv(POTATOES_HASHTAGS_AMBIGUOUS_PATH)
    potatoes = df['POTATOES']
    potatoes = potatoes.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    if n < 0:
        n = len(potatoes)
    return list(potatoes)[:n]

def MEANINGLESS_HASHTAGS_LIST():
    df = pd.read_csv(MEANINGLESS_HASHTAGS_PATH)
    hashtags = df['HASHTAGS']
    hashtags = hashtags.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    return list(hashtags)

def SEARCH_HASHTAGS_LIST():
    df = pd.read_csv(SEARCH_HASHTAGS_PATH)
    hashtags = df['HASHTAGS']
    hashtags = hashtags.map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    return list(hashtags)

def POTATOES_HASHTAGS_CLEAN(n = -1):
    df = pd.read_csv(POTATOES_HASHTAGS_AMBIGUOUS_PATH)
    if (n>0):
        df = df[:n]
    df['POTATOES'] = df['POTATOES'].map(lambda text: text.replace(' ', '')).map(lambda text: text.lower())
    df['HASHTAG'] = df['HASHTAG'].apply(lambda x: get_list(x))
    df['CLEAN'] = df['CLEAN'].apply(lambda x: get_list(x))
    return df

def QUARTER_RESULTS(quarter):
    path = os.path.join(PATHS_TO_QUARTERS, quarter + '.csv')
    return read_result_csv(path)

def QUARTER_CLEANED_RESULTS(quarter):
    path = os.path.join(POTATOES_CLEANED_DIR, quarter + '.csv')
    return read_result_csv(path)

def make_dirs():
  dirs = [HASHTAGS_PER_USER_DIR, POSTS_DIR_JSON, CLUSTERS_DIR_JSON, HASHTAG_FREQUENCY_DIR_JSON, CLUSTERS_DIR_JSON, HASHTAG_TOP_DIR, POTATOES_CLEANED_DIR, CLEANED_DIR, HASHTAG_FREQUENCY_DIR, GREEDY_MODULARITY_DIR, HASHTAG_FREQUENCY_DIR_ALL]
  for dir in dirs: 
    if not os.path.exists(dir):
        os.makedirs(dir)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

