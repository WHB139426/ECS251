import asyncio
import aiofiles
import numpy as np
from src.interfaces import DataLoader
from src import config

class AsyncDataLoader(DataLoader):
    async def _process_one_file(self, filepath):
        # 1. 真正的异步 IO (Non-blocking)
        async with aiofiles.open(filepath, 'rb') as f:
            _ = await f.read()
            
        # 2. CPU 任务处理 (关键点：不能阻塞 Event Loop)
        # 我们必须把 CPU 密集型任务扔到 ThreadPool 里去跑
        if self.matrix_size > 0:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._cpu_task_static, self.matrix_size)
            
        return filepath

    # 静态方法，方便 Executor 调用
    @staticmethod
    def _cpu_task_static(matrix_size):
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        np.dot(a, b)

    async def _run_all(self, files):
        # 创建所有协程任务
        tasks = [self._process_one_file(f) for f in files]
        # 并发执行
        await asyncio.gather(*tasks)

    def load_and_process(self, files):
        # 启动 Event Loop
        asyncio.run(self._run_all(files))