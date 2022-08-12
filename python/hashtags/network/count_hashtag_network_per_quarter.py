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

  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  for index, file in enumerate(files):
    print ('file no:', index+1)
    quarter_name = file.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    print ('>> now processing:', quarter_name)
    df = read_result_csv(file)
    frequency_csv_path = '../../data/processed/hashtag_frequency_onevoteperuser/' + quarter_name + '.csv'
    df_frequency = pd.read_csv(frequency_csv_path, names=['hashtag', 'count'], header=None)
    out_csv = os.path.join(os.path.join(out_dir, quarter_name + '.csv'))
    count_hashtag_network(df, df_frequency, 100, out_csv, True)
