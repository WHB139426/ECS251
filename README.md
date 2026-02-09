# Comparative Analysis of OS Concurrency Models for AI Data Pipelines

## Project Overview
This project investigates the performance trade-offs of different **Operating System concurrency primitives**: Threads, Processes, and Asynchronous I/O, in the context of **high-throughput Multimodal AI data loading**.

Modern AI training pipelines often suffer from "GPU Starvation" due to inefficient data ingestion. Our goal is to benchmark these concurrency models under varying ratios of **I/O-bound** (disk reading) and **CPU-bound** (data augmentation/decoding) tasks to identify the optimal strategy for Linux-based environments.

## Project Structure
The project is designed with a modular architecture to allow easy swapping of concurrency backends.
```text
ECS251/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── data/                   # Generated synthetic data (ignored in git)
├── logs/                   # Benchmark results and system logs
└── src/
    ├── config.py           # Centralized configuration (Matrix size, Workers)
    ├── generate_data.py    # Synthetic dataset generator
    ├── interfaces.py       # Abstract Base Classes (Loader Interface)
    ├── utils.py            # Timing, Logging, and Decorators
    └── loaders/            # Concurrency Implementations
        ├── __init__.py
        ├── sync_loader.py    # Synchronous implementation
        ├── thread_loader.py  # ThreadPool implementation
        ├── process_loader.py # ProcessPool implementation (TBD)
        └── async_loader.py   # AsyncIO implementation (TBD)
```

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.8+ installed. Install the required dependencies:

```bash
conda create -n ecs251 python=3.10.11
conda activate ecs251
git clone git@github.com:WHB139426/ECS251.git
cd ECS251
pip install -r requirements.txt
```

### 2. Generate Synthetic Dataset

Before running benchmarks, generate the mock "video/image" data. This script creates binary files with random sizes (default 1MB - 10MB) in the `data/` directory to simulate variable video frame payloads.

```bash
python -m src.generate_data
```

### 3. Run the Benchmark (Baseline)

Currently, the **Synchronous** and **Thread Pool** loaders are implemented as the baseline.

```bash
# Run the Synchronous loader
python -m src.main --mode sync
# Run the ThreadPool loader
python -m src.main --mode thread
```

*(Note: Full benchmarking suite with Process and Async modes will be available in following weeks).*

## Configuration

You can adjust the workload characteristics in `src/config.py` to simulate different AI tasks:

* **`MATRIX_SIZE`**: Controls CPU intensity.
* `0`: Pure I/O testing (Disk speed & context switch overhead).
* `200`: Mixed Workload (Realistic preprocessing).
* `500+`: CPU-bound (Stress-testing the GIL).
* **`NUM_WORKERS`**: Number of threads/processes to spawn.
* **`NUM_FILES`**: Total dataset size.

## Roadmap & Milestones

**Current Progress:** 
* Infrastructure setup & Architecture design.
* Abstract Interface definition (`DataLoader` class).
* Data Generation logic.
* ThreadPool and Synchronous baseline implementation.

**Next steps:** 
* Implementation of Multiprocessing (IPC handling).
* Implementation of AsyncIO (Coroutines & Event Loop).
* Automated benchmarking suite.
* Integration with OS metrics (`vmstat`, `pidstat`).
* Final analysis.
* Visualization of Throughput vs. Latency.
* Report generation.
