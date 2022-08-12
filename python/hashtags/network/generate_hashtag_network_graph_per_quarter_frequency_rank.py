import sys
sys.path.append('..')
from glob import glob
import os
from hashtag_network import generate_network_graph_rank
import pandas as pd

if __name__ == '__main__':
    files = sorted( glob('../../data/processed/hashtag_network/*.csv') )
    out_dir = '../../data/processed/hashtag_network_graphs'
    path_frequency = '../../data/processed/hashtag_frequency_plots_onevoteperuser/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for index, file in enumerate(files[:1]):
        print ('file no:', index+1)
        quarter_name = file.split('/')[-1].replace('.csv','')
        print ('>> now processing:', quarter_name)
        df_network = pd.read_csv(file)
        df_rank = pd.read_csv(path_frequency + quarter_name + '.csv')
        n_nodes = 51
        out_file = os.path.join(out_dir,quarter_name + '_' + str(n_nodes))
        generate_network_graph_rank(df_network, df_rank, n_nodes, out_file)
