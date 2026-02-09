import os
import glob
from src import config
from src.utils import Timer, logger
from src.loaders.thread_loader import ThreadDataLoader

def main():
    # 1. 检查数据是否存在
    if not os.path.exists(config.DATA_DIR):
        logger.error(f"Data directory not found at {config.DATA_DIR}")
        logger.error("Please run 'python -m src.generate_data' first.")
        return

    # 2. 获取所有测试文件路径
    files = glob.glob(os.path.join(config.DATA_DIR, "*.bin"))
    if not files:
        logger.error("No data files found. Please generate data first.")
        return

    logger.info(f"Found {len(files)} files. Starting Benchmark...")
    logger.info(f"Mode: ThreadPool | Workers: {config.NUM_WORKERS} | Matrix Size: {config.MATRIX_SIZE}")

    # 3. 初始化 Loader
    loader = ThreadDataLoader(config.DATA_DIR, config.MATRIX_SIZE)

    # 4. 开始跑分
    with Timer("ThreadPool Benchmark"):
        # 这里实际上会调用 thread_loader.py 里写的逻辑
        loader.load_and_process(files)

if __name__ == "__main__":
    main()