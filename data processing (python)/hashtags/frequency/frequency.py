import pandas as pd
from nltk.probability import FreqDist


def group_by_user(df):
    # TO FIX to get most liked post by user
    # df = df.set_index('post_url').groupby('owner_id').agg(
    #     hashtags=pd.NamedAgg(column='hashtags', aggfunc='sum'), 
    #     post_count=pd.NamedAgg(column='shortcode', aggfunc='count'),
    #     most_liked_post = pd.NamedAgg(column='likes', aggfunc='idxmax')
    # )
    df = df.groupby('owner_id').agg(
        hashtags=pd.NamedAgg(column='hashtags', aggfunc='sum'), 
        post_count=pd.NamedAgg(column='shortcode', aggfunc='count'),
        # most_liked_post = pd.NamedAgg(column='likes', aggfunc='idxmax')
    )
    df = df.sort_values(by=['post_count'], ascending=False)
    df['hashtags'] = df['hashtags'].apply(lambda x: list(set(x)))
    return df


def count_hashtag_frequency(df):
    hashtags = list(df['hashtags'])
    flat_list = [item.lower() for sublist in hashtags for item in sublist]
    print(len(flat_list))
    
    fdist = FreqDist(flat_list)
    return fdist.most_common()