
import sys
sys.path.append('..')
import pandas as pd
import os
from glob import glob
from nltk.probability import FreqDist
import csv
from utils.utils import get_word_list


def extract_words(in_file, out_file):
    df = pd.read_csv(in_file)
    df['words'] = df['caption'].apply(get_word_list)
    words = list(df['words'])
    flat_list = [item.lower() for sublist in words for item in sublist]

    fdist = FreqDist(flat_list)
    print(fdist.most_common(10))

    with open(out_file, "w+") as fp:
      writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
      writer.writerows(fdist.most_common())

if __name__ == '__main__':
  files = sorted( glob('../../data/Instagram-API/Feed/Actors/hashtag-*/result/result.csv') )
  out_dir = '../../data/processed/word_frequency'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  idx = 1
  for file in files:
    print ('file no:', idx)
    idx += 1
    quarter_name = file.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    print ('>> now processing:', quarter_name)
    out_csv = out_dir + '/' + quarter_name + '.csv'    
    extract_words(file, out_csv)
