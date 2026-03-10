import asyncio
import aiofiles
import numpy as np
from src.interfaces import DataLoader

class AsyncDataLoader(DataLoader):
    async def _process_one_file(self, filepath):
        async with aiofiles.open(filepath, 'rb') as f:
            _ = await f.read()
            
        if self.matrix_size > 0:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._cpu_task_static, self.matrix_size)
            
        return filepath

    @staticmethod
    def _cpu_task_static(matrix_size):
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        np.dot(a, b)

    async def _run_all(self, files):
        tasks = [self._process_one_file(f) for f in files]
        await asyncio.gather(*tasks)

    def load_and_process(self, files):
        asyncio.run(self._run_all(files))