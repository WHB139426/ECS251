import os
import glob
import argparse
from src import config
from src.utils import Timer, logger

# 导入所有的 Loaders
from src.loaders.sync_loader import SyncDataLoader
from src.loaders.thread_loader import ThreadDataLoader
from src.loaders.process_loader import ProcessDataLoader
from src.loaders.async_loader import AsyncDataLoader

def main():
    # 1. 解析参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, required=True, 
                        choices=['sync', 'thread', 'process', 'async'])
    args = parser.parse_args()

    # 2. 检查数据
    if not os.path.exists(config.DATA_DIR):
        logger.error(f"Data directory not found at {config.DATA_DIR}")
        return
    
    files = glob.glob(os.path.join(config.DATA_DIR, "*.bin"))
    if not files:
        logger.error("No data files found. Please generate data first.")
        return

    logger.info(f"Starting Benchmark | Mode: {args.mode.upper()} | Workers: {config.NUM_WORKERS} | Matrix: {config.MATRIX_SIZE}")

    # 3. 初始化对应的 Loader
    if args.mode == 'sync':
        loader = SyncDataLoader(config.DATA_DIR, config.MATRIX_SIZE)
    elif args.mode == 'thread':
        loader = ThreadDataLoader(config.DATA_DIR, config.MATRIX_SIZE)
    elif args.mode == 'process':
        loader = ProcessDataLoader(config.DATA_DIR, config.MATRIX_SIZE)
    elif args.mode == 'async':
        loader = AsyncDataLoader(config.DATA_DIR, config.MATRIX_SIZE)

    # 4. 跑分
    with Timer(f"{args.mode} Benchmark"):
        loader.load_and_process(files)

if __name__ == "__main__":
    main()