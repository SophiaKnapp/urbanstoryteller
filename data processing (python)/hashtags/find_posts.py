
from decimal import Clamped
import sys

sys.path.append('..')
from utils.paths import QUARTER_RESULTS, CLUSTERS_DIR
import pandas as pd
import os
from utils.paths import make_dirs
from utils.utils import write_df_to_csv





def find_posts_in_cluster(df, out_dir, cluster_hashtags):
    # df['rank'] = df.apply(lambda row: [hashtag for hashtag in row.hashtags if hashtag in hatags])
    df = df[['post_url', 'owner_id', 'hashtags', 'caption']]
    df['rank'] = df['hashtags'].apply(lambda row: post_accuracy(row, cluster_hashtags))
    df = df.sort_values(by=['rank'], ascending=False)
    print(len(df))
    df.drop(df[df['rank'] == 0].index, inplace = True)
    print(len(df))
    print(df[:10])

    cluster = str(cluster_hashtags)

    write_df_to_csv(df, quarter + cluster + '_rank', out_dir)

    df = df.groupby('owner_id').agg(
        hashtags=pd.NamedAgg(column='hashtags', aggfunc='sum'), 
        post_count=pd.NamedAgg(column='post_url', aggfunc='count'),
        # most_liked_post = pd.NamedAgg(column='likes', aggfunc='idxmax')
    )

    print(df.columns)

    df = df.sort_values(by=['post_count'], ascending=False)

    write_df_to_csv(df, quarter + cluster + '_users', out_dir)


def post_accuracy(hashtags, cluster_hashtags):
    
    # print(count)
    if(len(hashtags) != 0): 
        list =[hashtag for hashtag in hashtags if hashtag in cluster_hashtags]
        return len(list)/len(hashtags)
    else:
        return 0




quarter = "Neuperlach"

# out_dir = os.path.join(CLUSTERS_DIR, quarter)
# make_dirs()


df = QUARTER_RESULTS(quarter)

# find_posts_in_cluster(df,out_dir, ['hiphop', 'music', 'musik', 'deutschrap', 'rap'])

# find_posts_in_cluster(df, out_dir, ['mvg', 'ubahn', 'bus', 'mvv', 'mvgmünchen'])
find_posts_in_cluster(df, out_dir, ['sun', 'sommer', 'sonne', 'summer'])

# find_posts_in_cluster(df, out_dir, ['n', 'ubahn', 'bus', 'mvv', 'mvgmünchen'])






# find_posts_in_cluster(df, out_dir, ['plattenbauromantik', 'brutalism', 'beton', 'plattenbau', 'wohnring'])
# find_posts_in_cluster(df, out_dir, ['wohnen', 'wohnung', 'neubau', 'mond', 'balkon', 'marxzentrum','immobilienmakler', 'immobilien', 'wohnring', 'hochhaus'])
# find_posts_in_cluster(df, out_dir, ['schule', 'communitykitchen', 'shaere', 'kultur', 'nachhaltigkeit', 'kinder', 'bildung', 'gemeinsam', 'zukunft'])
# find_posts_in_cluster(df, out_dir, ['festival', 'drama', 'theatre', 'peppertheater', 'theater'])
# find_posts_in_cluster(df, out_dir, ['coffee', 'kaffee', 'cafe'])
# find_posts_in_cluster(df, out_dir, ['friseur', 'hairstyle', 'hair'])
# find_posts_in_cluster(df, out_dir, ['photography', 'nature', 'clouds', 'blue', 'sunset', 'sonnenuntergang', 'naturephotography', 'herbst', 'schnee', 'winter', 'snow', 'flowers', 'trees', 'spring', 'himmel', 'alpen'])









