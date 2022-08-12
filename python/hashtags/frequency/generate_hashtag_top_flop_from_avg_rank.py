import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_frequency_plot_simpler import plot_all_frequencies



import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_frequency_plot_simpler import plot_all_frequencies
import pandas as pd


def get_rank_diff(files, file_all, out_dir):
    idx = 1
    # colnames=['hashtag', 'count'] 
    # df_all_frequencies = add_rank_column(df_all_frequencies)

    df = pd.read_csv(file_all)
    df = df.set_index('hashtag')
        # df = pd.read_csv(file_all, names=colnames)

    print(df[:10])

    for index,f in enumerate(files):
      quarter = f.split('/')[-1]
      print ('file no:', idx)
      idx += 1
      print ('>> now processing:', f)
      df_new = pd.read_csv(f)
      df_new = df_new[['hashtag', 'rank_quarter', 'rank_all']]
      df_new = df_new.set_index('hashtag')
      # df_new = df_new[['hashtag', 'rank_quarter']]
      # print(df_new[:10])
      # df_new = df_new.set_index('hashtag')
      # df = add_rank_column(df)
      df_new = df_new.join(df, lsuffix='_new', rsuffix=quarter)

      df_new = df_new[df_new['rank_average'].notna()]
      # generate_graph(df, quarter, out_dir)
      
      df_new['rank_diff'] = df_new['rank_average'] - df_new['rank_quarter']
      df_new.sort_values(by=['rank_diff'], inplace=True)
      print(df_new[:10])
      df_new.to_csv(os.path.join(out_dir, quarter))


    return

  

if __name__ == '__main__':
  files = sorted( glob('../../../data/processed/hashtag_frequency_plots/*.csv') )
  file_all = '../../../data/processed/hashtag_frequency_plots_AVG/ordered_by_rank.csv'

  out_dir = '../../../data/processed/hashtag_frequency_top_flop'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  get_rank_diff(files, file_all, out_dir)
