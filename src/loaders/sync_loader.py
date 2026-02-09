from src.interfaces import DataLoader

class SyncDataLoader(DataLoader):
    def process_file(self, filepath):
        with open(filepath, 'rb') as f:
            _ = f.read()
        self.cpu_bound_task()
        return filepath

    def load_and_process(self, files):
        return [self.process_file(f) for f in files]