import ast
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
import pandas as pd
import os
from glob import glob
import csv
import networkx as nx

def get_literals(x):
  try:
    return ast.literal_eval(x)
  except:
    return []

def get_list(x):
  if isinstance(x, float):
    return []
  else:
    return x.split(', ')


def get_word_list(x):
  if isinstance(x, str):
    tokens = word_tokenize(x)
    tokens = [w.lower() for w in tokens]
    # words = [word for word in tokens if word.isalpha()]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    stop_words = set(stopwords.words('german'))
    words = [w for w in words if not w in stop_words]

    # print(words[:10])
    return words
  else:
    return []


def read_result_csv(path):
  df = pd.read_csv(path, header=0)
  if 'hashtags' in df.columns:
    df['hashtags'] = df['hashtags'].map(get_literals)
    df['hashtags'] = df['hashtags'].map(lambda x: [item.lower() for item in x])
  return df

def load_dataframe(dir, name):
  path = os.path.join(dir, name + '.csv')
  print ('>> now loading:', name)
  df = read_result_csv(path)
  return df

def load_dataframes(dir, n=-1):
    paths = sorted(glob(dir + '/*'))
    if n == -1:
        n = len(paths)
    dfs = {}
    for path in paths[:n]:
        name = path.split('/')[-1].replace('.csv','')
        print ('>> now loading:', name)
        df = read_result_csv(path)
        dfs[name] = df
    return dfs


def write_df_to_csv(df, name, dir):
  df.to_csv(os.path.join(dir, name + '.csv'), index=False)


def write_list_to_csv(list, name, dir, columns=[]):
      with open(os.path.join(dir, name + '.csv'), "w+") as fp:
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        if columns != []:
          writer.writerow(columns)
        writer.writerows(list)


def write_dict_to_csv(dict, name, dir, columns=[]):
    file_name = os.path.join(dir, name + '.csv')
    with open(file_name, "w+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for new_k, new_v in dict.items():
            writer.writerow([new_k, new_v])


def write_graph_to_file(G, name, dir):
  file_name = os.path.join(dir, name + '.gpickle')
  nx.write_gpickle(G, file_name)

def load_graph(dir, name):
  G = nx.read_gpickle(os.path.join(dir, name + '.gpickle'))
  return G