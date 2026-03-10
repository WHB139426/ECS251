import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from src.interfaces import DataLoader
from src import config

def _process_worker(args):
    filepath, matrix_size = args
    
    with open(filepath, 'rb') as f:
        _ = f.read()
        
    if matrix_size > 0:
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        np.dot(a, b)
        
    return filepath

class ProcessDataLoader(DataLoader):
    def load_and_process(self, files):
        # args_list = [("data/file1.bin", 200), ("data/file2.bin", 200), ...]
        args_list = [(f, self.matrix_size) for f in files]
        
        with ProcessPoolExecutor(max_workers=config.NUM_WORKERS) as executor:
            list(executor.map(_process_worker, args_list))