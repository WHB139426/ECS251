from concurrent.futures import ThreadPoolExecutor
from src.interfaces import DataLoader
from src import config  # <--- 新增引入

class ThreadDataLoader(DataLoader):
    def process_file(self, filepath):
        # IO Operation
        with open(filepath, 'rb') as f:
            _ = f.read()
        # CPU Operation
        self.cpu_bound_task()
        return filepath

    def load_and_process(self, files):
        with ThreadPoolExecutor(max_workers=config.NUM_WORKERS) as executor:
            list(executor.map(self.process_file, files))