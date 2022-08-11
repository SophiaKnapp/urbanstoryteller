
import sys
sys.path.append('..')
import os
from glob import glob
from hashtag_frequency_all_quarters import count_hashtag_frequency_all_quarters

if __name__ == '__main__':
  files = sorted( glob('../../data/Instagram-API/Feed/Actors/hashtag-*/result/result.csv') )
  out_dir = '../../data/processed/hashtag_frequency_all'
  out_csv = os.path.join(out_dir, 'hashtag_frequency_all.csv')

  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  one_vote_per_user = False
  count_hashtag_frequency_all_quarters(files, out_csv, one_vote_per_user)