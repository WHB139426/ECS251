import pandas as pd
from tqdm import tqdm
import os
import glob
import asyncio

from src import config
from src.loaders.sync_loader import SyncDataLoader
from src.loaders.thread_loader import ThreadDataLoader
from src.loaders.process_loader import ProcessDataLoader
from src.loaders.async_loader import AsyncDataLoader
from src.utils import Timer
from src.monitor import ResourceMonitor  # <--- 新增导入

# === config ===
MATRIX_SIZES = [0, 100, 300, 500]
WORKER_COUNTS = [1, 2, 4, 8]
MODES = ['sync', 'thread', 'process', 'async']

def run_suite():
    print("🚀 Starting Automated Experiment Suite with OS Monitoring...")
    
    files = glob.glob(os.path.join(config.DATA_DIR, "*.bin"))
    if not files:
        print("Error: No data.")
        return

    results = []
    total_runs = len(MATRIX_SIZES) * len(WORKER_COUNTS) * len(MODES)
    pbar = tqdm(total=total_runs)

    for m_size in MATRIX_SIZES:
        for workers in WORKER_COUNTS:
            config.MATRIX_SIZE = m_size
            config.NUM_WORKERS = workers
            
            for mode in MODES:
                if mode == 'sync':
                    loader = SyncDataLoader(config.DATA_DIR, m_size)
                elif mode == 'thread':
                    loader = ThreadDataLoader(config.DATA_DIR, m_size)
                elif mode == 'process':
                    loader = ProcessDataLoader(config.DATA_DIR, m_size)
                elif mode == 'async':
                    loader = AsyncDataLoader(config.DATA_DIR, m_size)
                
                try:
                    with ResourceMonitor() as monitor:
                        with Timer("Exp", suppress_log=True) as t:
                            loader.load_and_process(files)
                    
                    results.append({
                        "Mode": mode,
                        "Matrix_Size": m_size,
                        "Workers": workers,
                        "Time_Sec": t.duration,
                        "Throughput": len(files) / t.duration,
                        "Peak_Memory_MB": monitor.peak_memory_mb,      # 新增
                        "Context_Switches": monitor.total_ctx_switches # 新增
                    })
                except Exception as e:
                    print(f"Failed: {mode} w={workers} m={m_size} | {e}")
                
                pbar.update(1)
    
    pbar.close()
    
    df = pd.DataFrame(results)
    output_file = "experiment_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Experiments finished! Saved to {output_file}")

if __name__ == "__main__":
    run_suite()