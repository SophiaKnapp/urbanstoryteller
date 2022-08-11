import pandas as pd
from glob import glob
import os


def find_hashtag(files, out_dir, hashtag):
  idx = 1
  colnames=['hashtag', 'count'] 
  count_per_quarter = dict()
  for index,f in enumerate(files):

    quarter = f.split('/')[-1].replace('.csv','')
    print ('file no:', idx)
    idx += 1
    print ('>> now processing:', f)
    df = pd.read_csv(f, names=colnames, header=None)
    df.drop(df[df['count'] < 10].index, inplace = True)
    row = df[df['hashtag']==hashtag]['count']

    total_count = df['count'].sum()

    if (len(row) != 0):
      n = row.values[0]
      count_per_quarter[quarter] = n /total_count
  

  df = pd.DataFrame.from_dict(count_per_quarter, orient='index', columns=['count'])
  df = df.sort_values(by=['count'], ascending=False)

  out_path = os.path.join(out_dir, hashtag + '_relative.csv')
  df.to_csv(out_path)
  return

def rank(row):
    return (row.name+1)*row['count']
  
if __name__ == '__main__':
  files = sorted( glob('../../data/processed/hashtag_frequency_onevoteperuser/*') )
  file_all_frequencies = '../../data/processed/hashtag_frequency_all/hashtag_frequency_all_onevoteperuser.csv'
  out_dir = '../../data/processed/hashtag_count_per_quarter'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  # find_hashtag(files, out_dir, 'natur')
  find_hashtag(files, out_dir, 'kunst')
  # find_hashtag(files, out_dir, 'natur')
