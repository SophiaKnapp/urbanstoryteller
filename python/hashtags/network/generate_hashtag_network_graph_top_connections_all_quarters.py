import sys 
sys.path.append('..')
from glob import glob
import os
from hashtag_network import generate_network_graph
import pandas as pd

if __name__ == '__main__':
    files = sorted( glob('../../data/processed/hashtag_network/*.csv') )
    out_dir = '../../data/processed/hashtag_network_graphs'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    df = pd.DataFrame()

    top_n = 5

    for index, file in enumerate(files):
        print ('file no:', index+1)
        quarter_name = file.split('/')[-1].replace('.csv','')
        print ('>> now processing:', quarter_name)
        df_new = pd.read_csv(file)

        df = df.append(df_new[:top_n],ignore_index=True)
        print(len(df))

    n_nodes = 500
    out_file = os.path.join(out_dir,'top_' + str(top_n) + '_' + str(n_nodes))
    generate_network_graph(df, n_nodes, out_file)