import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_network import count_hashtag_network
import pandas as pd
from utils.utils import read_result_csv


if __name__ == '__main__':
  files = sorted( glob('../../data/Instagram-API/Feed/Actors/hashtag-*/result/result.csv') )
  out_dir = '../../data/processed/hashtag_network'

  file_all_frequencies = '../../data/processed/hashtag_frequency_all/hashtag_frequency_all_onevoteperuser.csv'
  df_frequency = pd.read_csv(file_all_frequencies, names=['hashtag', 'count'], header=None)


  df = pd.DataFrame()
  idx = 1
  for file in files:
    print ('file no:', idx)
    idx += 1
    quarter_name = file.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    print ('>> now processing:', quarter_name)
    df_new = read_result_csv(file)
    df_new_hashtags = df_new[['owner_id','shortcode','hashtags']]
    df = df.append(df_new_hashtags,ignore_index=True)

  print(df[:10])
  print(len(df))
  df = df.drop_duplicates(subset=['shortcode'])
  print(len(df))
  n_nodes = 200
  out_csv = os.path.join(out_dir, 'network_count_all_' + str(n_nodes) + '.csv')
  count_hashtag_network(df, df_frequency, n_nodes, out_csv, True)