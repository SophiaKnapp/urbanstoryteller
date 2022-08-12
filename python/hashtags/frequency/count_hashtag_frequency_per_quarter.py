import sys
sys.path.append('..')
import os
from glob import glob
from hashtag_frequency_per_quarter import count_hashtags

if __name__ == '__main__':
  files = sorted( glob('../../data/Instagram-API/Feed/Actors/hashtag-*/result/result.csv') )
  out_dir = '../../data/processed/hashtag_frequency'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  idx = 1
  for file in files:
    print ('file no:', idx)
    idx += 1
    quarter_name = file.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    print ('>> now processing:', quarter_name)
    out_csv = out_dir + '/' + quarter_name + '.csv'
    one_vote_per_user = False    
    count_hashtags(file, out_csv, one_vote_per_user)
