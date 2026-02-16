import pandas as pd
from tqdm import tqdm
import os
import glob
import asyncio

from src import config
# 直接导入类，绕过 main.py 的命令行解析，方便脚本调用
from src.loaders.sync_loader import SyncDataLoader
from src.loaders.thread_loader import ThreadDataLoader
from src.loaders.process_loader import ProcessDataLoader
from src.loaders.async_loader import AsyncDataLoader
from src.utils import Timer

# === 实验配置网格 ===
MATRIX_SIZES = [0, 100, 300, 500]  # 从纯IO到高计算
WORKER_COUNTS = [1, 2, 4, 8]       # 并发数
MODES = ['sync', 'thread', 'process', 'async'] # 要测试的模式

def run_suite():
    print("🚀 Starting Automated Experiment Suite...")
    
    files = glob.glob(os.path.join(config.DATA_DIR, "*.bin"))
    if not files:
        print("Error: No data.")
        return

    results = []
    
    # 进度条总数
    total_runs = len(MATRIX_SIZES) * len(WORKER_COUNTS) * len(MODES)
    pbar = tqdm(total=total_runs)

    for m_size in MATRIX_SIZES:
        for workers in WORKER_COUNTS:
            # 动态修改全局配置 (Monkey Patching)
            config.MATRIX_SIZE = m_size
            config.NUM_WORKERS = workers
            
            for mode in MODES:
                # 实例化 Loader
                if mode == 'sync':
                    # Sync 模式通常不需要 worker 数量，但为了格式统一我们还是传参
                    # 注意：SyncLoader 内部通常是单线程，会忽略 workers 参数，
                    # 但在画图时，我们可以把它画成一条横线，或者只看 workers=1 的数据点。
                    loader = SyncDataLoader(config.DATA_DIR, m_size)
                if mode == 'thread':
                    loader = ThreadDataLoader(config.DATA_DIR, m_size)
                elif mode == 'process':
                    loader = ProcessDataLoader(config.DATA_DIR, m_size)
                elif mode == 'async':
                    loader = AsyncDataLoader(config.DATA_DIR, m_size)
                
                # 运行并计时
                try:
                    with Timer("Exp", suppress_log=True) as t:
                        loader.load_and_process(files)
                    
                    # 记录数据
                    results.append({
                        "Mode": mode,
                        "Matrix_Size": m_size,
                        "Workers": workers,
                        "Time_Sec": t.duration,
                        "Throughput": len(files) / t.duration
                    })
                except Exception as e:
                    print(f"Failed: {mode} w={workers} m={m_size} | {e}")
                
                pbar.update(1)
    
    pbar.close()
    
    # 保存结果
    df = pd.DataFrame(results)
    output_file = "experiment_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Experiments finished! Saved to {output_file}")

if __name__ == "__main__":
    run_suite()