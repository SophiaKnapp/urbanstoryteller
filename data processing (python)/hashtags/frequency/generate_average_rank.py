import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_frequency_plot_simpler import plot_all_frequencies
import pandas as pd


def get_average_rank(files, file_all, out_dir):
    idx = 1
    colnames=['hashtag', 'count'] 
    # df_all_frequencies = add_rank_column(df_all_frequencies)

    df = pd.read_csv(file_all, names=colnames)
    df.drop(df[df['count'] < 10].index, inplace = True)


    print(df[:10])


    df = df.set_index('hashtag')

    print(df[:10])


    for index,f in enumerate(files):
      quarter = f.split('/')[-1]
      print ('file no:', idx)
      idx += 1
      print ('>> now processing:', f)
      df_new = pd.read_csv(f)
      df_new = df_new[['hashtag', 'rank_quarter']]
      # df_new = df_new.set_index('hashtag')
      # df = add_rank_column(df)
      df = df.join(df_new.set_index('hashtag'), lsuffix='old', rsuffix=index)
      # generate_graph(df, quarter, out_dir)


    print(df[:10])
    df = df.fillna(0)
    print(df[:10])

    df['sum'] = df[df.columns[1:]].apply(
      sum,
      axis=1
    )

    df['rank_average'] = df['sum']/len(files)

    

    df = df[['count','rank_average']]

    df.to_csv(out_dir+'/ordered_by_count.csv')

    df.sort_values(by=['rank_average'], ascending=False, inplace=True)

    df.to_csv(out_dir+'/ordered_by_rank.csv')


    return

  

if __name__ == '__main__':
  files = sorted( glob('../../../data/processed/hashtag_frequency_plots/*.csv') )
  file_all = '../../../data/processed/hashtag_frequency_all/hashtag_frequency_all_onevoteperuser.csv'

  out_dir = '../../../data/processed/hashtag_frequency_plots_AVG'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  get_average_rank(files, file_all, out_dir)
