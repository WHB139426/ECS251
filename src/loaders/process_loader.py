import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from src.interfaces import DataLoader
from src import config

# [关键点] Worker必须定义在顶层，不能在类里面，否则多进程无法序列化(Pickle)
def _process_worker(args):
    filepath, matrix_size = args
    
    # 1. 模拟 IO
    with open(filepath, 'rb') as f:
        _ = f.read()
        
    # 2. 模拟 CPU (矩阵乘法)
    if matrix_size > 0:
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        np.dot(a, b)
        
    return filepath

class ProcessDataLoader(DataLoader):
    def load_and_process(self, files):
        # 多进程需要传参数比较麻烦，我们将参数打包成 tuple
        # args_list = [("data/file1.bin", 200), ("data/file2.bin", 200), ...]
        args_list = [(f, self.matrix_size) for f in files]
        
        with ProcessPoolExecutor(max_workers=config.NUM_WORKERS) as executor:
            # map 会自动分发任务给子进程
            list(executor.map(_process_worker, args_list))