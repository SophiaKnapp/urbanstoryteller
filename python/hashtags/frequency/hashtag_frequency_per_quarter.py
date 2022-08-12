import sys
sys.path.append('..')
import pandas as pd
from nltk.probability import FreqDist
import csv
from utils.utils import get_literals


def count_hashtags(in_file, out_file, one_vote_per_user):
    df = pd.read_csv(in_file)
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
    print(len(flat_list))

    fdist = FreqDist(flat_list)
    print(fdist.most_common(10))

    with open(out_file, "w+") as fp:
      writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
      writer.writerows(fdist.most_common())