from concurrent.futures import ThreadPoolExecutor
from src.interfaces import DataLoader
import os

class ThreadDataLoader(DataLoader):
    def process_file(self, filepath):
        # IO Operation
        with open(filepath, 'rb') as f:
            _ = f.read()
        # CPU Operation
        self.cpu_bound_task()
        return filepath

    def load_and_process(self, files):
        # We assume 4 workers for now
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(self.process_file, files))