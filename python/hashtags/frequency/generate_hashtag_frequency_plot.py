import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_frequency_plot import plot_all_frequencies

if __name__ == '__main__':
  files = sorted( glob('../../data/processed/hashtag_frequency/*') )
  file_all_frequencies = '../../data/processed/hashtag_frequency_all/hashtag_frequency_all.csv'
  out_dir = '../../data/processed/hashtag_frequency_plots'
  if not os.path.exists(out_dir):
      os.makedirs(out_dir)

  plot_all_frequencies(files, file_all_frequencies, out_dir)