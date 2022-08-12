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

    for index, file in enumerate(files[:1]):
        print ('file no:', index+1)
        quarter_name = file.split('/')[-1].replace('.csv','')
        print ('>> now processing:', quarter_name)
        df = pd.read_csv(file)
        n_nodes = 51
        out_file = os.path.join(out_dir,quarter_name + '_' + str(n_nodes))
        generate_network_graph(df, n_nodes, out_file)
