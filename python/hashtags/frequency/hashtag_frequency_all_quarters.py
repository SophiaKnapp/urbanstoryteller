
import sys
sys.path.append('..')
import pandas as pd
from nltk.probability import FreqDist
import csv
from utils.utils import get_literals

def count_hashtag_frequency_all_quarters(files, out_csv, one_vote_per_user):
  df = pd.DataFrame()
  idx = 1
  for file in files:
    print ('file no:', idx)
    idx += 1
    quarter_name = file.replace('../../data/Instagram-API/Feed/Actors/hashtag-','').replace('/result/result.csv', '')
    print ('>> now processing:', quarter_name)
    df_new = pd.read_csv(file)
    df_new_hashtags = df_new[['owner_id','shortcode','hashtags']]
    df = df.append(df_new_hashtags,ignore_index=True)

  print(df[:10])
  print(len(df))
  df = df.drop_duplicates(subset=['shortcode'])
  print(len(df))

  df = df[['owner_id', 'shortcode', 'hashtags']]
  df['hashtags'] = df['hashtags'].apply(lambda x: get_literals(x))

  if one_vote_per_user:
    df = df.groupby('owner_id').agg(
      hashtags=pd.NamedAgg(column='hashtags', aggfunc='sum'), 
      post_count=pd.NamedAgg(column='shortcode', aggfunc='count')
    )

    df = df.sort_values(by=['post_count'], ascending=False)
    df['hashtags'] = df['hashtags'].apply(lambda x: list(set(x)))

  
  hashtags = list(df['hashtags'])
  flat_list = [item.lower() for sublist in hashtags for item in sublist]

  fdist = FreqDist(flat_list)
  print(fdist.most_common(10))

  with open(out_csv, "w+") as fp:
    writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
    writer.writerows(fdist.most_common())