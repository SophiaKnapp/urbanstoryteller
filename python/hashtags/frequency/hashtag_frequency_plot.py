import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_all_frequencies(files, file, out_dir):
  idx = 1
  colnames=['hashtag', 'count'] 
  df_all_frequencies = pd.read_csv(file,names=colnames, header=None)
  df_all_frequencies = add_rank_column(df_all_frequencies)

  for index,f in enumerate(files):
    quarter = f.split('/')[-1]
    print ('file no:', idx)
    idx += 1
    print ('>> now processing:', f)
    df = pd.read_csv(f, names=colnames, header=None)
    df = add_rank_column(df)

    df = df.set_index('hashtag').join(df_all_frequencies.set_index('hashtag'), lsuffix='_quarter', rsuffix='_all')
    generate_graph(df, quarter, out_dir)
    find_rank_diff(df, quarter, out_dir)
  return

def find_rank_diff(df, quarter, out_dir):
  df['rank_diff'] = df['rank_quarter'] - df['rank_all']
  df = df.sort_values(by=['rank_diff'])
  print(quarter)
  print(df[:5])
  print(df[-5:])
  out_path = os.path.join(out_dir, quarter)
  df.to_csv(out_path)

def generate_graph(df, quarter, out_dir):
  fig, ax = plt.subplots()

  ax.scatter(df['rank_quarter'], df['rank_all'])
  xy_line = (0, 1)
  ax.plot(xy_line, 'g-')
  ax.set_xlabel('Rank all')
  ax.set_ylabel('Rank quarter')
  num_words = 15
  df['rank_diff'] = df['rank_quarter'] - df['rank_all']
  df = df.sort_values(by=['rank_diff'])
  for i, txt in enumerate(df.index.values):
    if (i <num_words) or (i > len(df.index.values)-num_words):
      ax.annotate(txt, (df['rank_quarter'][i], df['rank_all'][i]), fontsize=5)
  plt.savefig(os.path.join(out_dir,quarter.replace('.csv','.png')), dpi=300)


def add_rank_column(df):
  df.drop(df[df['count'] < 10].index, inplace = True)
  df['rank'] = df.apply(rank, axis=1)
  max = df['rank'].max()
  df['rank'] = df['rank'].div(max)
  return df

def rank(row):
    return (row.name+1)*row['count']
