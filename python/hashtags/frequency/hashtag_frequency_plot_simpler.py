import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_all_frequencies(files, file, out_dir):
  idx = 1
  colnames=['hashtag', 'count'] 
  df_all_frequencies = pd.read_csv(file,names=colnames, header=None)
  # df_all_frequencies = add_rank_column(df_all_frequencies)

  treshold = 1/len(files)

  for index,f in enumerate(files):
    quarter = f.split('/')[-1]
    print ('file no:', idx)
    idx += 1
    print ('>> now processing:', f)
    df = pd.read_csv(f, names=colnames, header=None)
    # df = add_rank_column(df)

    df = df.set_index('hashtag').join(df_all_frequencies.set_index('hashtag'), lsuffix='_quarter', rsuffix='_all')
    # generate_graph(df, quarter, out_dir)
    find_diff(df, quarter, out_dir, treshold)
  return

def find_diff(df, quarter, out_dir, treshold):
  df.drop(df[df['count_quarter'] < 5].index, inplace = True)
  df['relevance'] = df['count_quarter']/df['count_all']
  df['rank'] = df['count_quarter'] * df['relevance']

  print(len(df))

  df_top = df[df['relevance']>treshold]
  df_flop = df[df['relevance']<treshold]

  print(len(df_top))
  print(len(df_flop))



  df_top = df_top.sort_values(by=['rank'], ascending=False)

  df_flop = df_flop.sort_values(by=['rank'])

  out_path_top = os.path.join(out_dir, 'top_' + quarter)
  out_path_flop = os.path.join(out_dir, 'flop_' + quarter)
  df_top.to_csv(out_path_top)
  df_flop.to_csv(out_path_flop)

# def add_rank_column(df):
#   df.drop(df[df['count'] < 10].index, inplace = True)
#   df['rank'] = df.apply(rank, axis=1)
#   max = df['rank'].max()
#   df['rank'] = df['rank'].div(max)
#   return df

# def rank(row):
#     return (row.name+1)*row['count']
