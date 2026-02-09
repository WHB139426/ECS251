import os
import glob
from src import config
from src.utils import Timer, logger
from src.loaders.thread_loader import ThreadDataLoader
from src.loaders.sync_loader import SyncDataLoader

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
    if args.mode == 'thread':
        loader = ThreadDataLoader(config.DATA_DIR, config.MATRIX_SIZE)
    elif args.mode == 'sync':
        loader = SyncDataLoader(config.DATA_DIR, config.MATRIX_SIZE)

    # 4. 开始跑分
    with Timer(f"{args.mode} Benchmark"):
        loader.load_and_process(files)

if __name__ == "__main__":

    import argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='thread', choices=['thread', 'sync'])
    args = parser.parse_args()

    logger.info(f"Mode: {args.mode} | ...")

    main()