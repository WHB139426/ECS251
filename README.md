# ECS-251 Project: Comparative Analysis of OS Concurrency Models for AI Data Pipelines 
## Project Overview
This project investigates the performance trade-offs of different Operating System concurrency primitives: Threads, Processes, and Asynchronous I/O, in the context of high-throughput Multimodal AI data loading.

Modern AI training pipelines often suffer from "GPU Starvation" due to inefficient data ingestion. Our goal is to benchmark these concurrency models under varying ratios of I/O-bound (disk reading) and CPU-bound (data augmentation/decoding) tasks to identify the optimal strategy for Linux-based environments.

Group Members: *Haibo Wang; Sihai Yu; Yuankai Li*

## Project Structure
The project is designed with a modular architecture to allow easy swapping of concurrency backends.
```text
ECS251/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── run_experiment.py       # Automated benchmarking suite (Iterates all configs)
├── data/                   # Generated synthetic data (ignored in git)
├── logs/                   # Benchmark results and system logs
└── src/
    ├── config.py           # Centralized configuration (Matrix size, Workers)
    ├── generate_data.py    # Synthetic dataset generator
    ├── interfaces.py       # Abstract Base Classes (Loader Interface)
    ├── utils.py            # Timing, Logging, and Decorators
    └── loaders/            # Concurrency Implementations
        ├── __init__.py
        ├── sync_loader.py    # Synchronous implementation (Baseline)
        ├── thread_loader.py  # ThreadPool implementation
        ├── process_loader.py # ProcessPool implementation (Multiprocessing)
        └── async_loader.py   # AsyncIO implementation (Coroutines)
```

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.10+ installed. Install the required dependencies:

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

You can run a specific concurrency model manually to verify behavior or debug.

```bash
# 1. Baseline: Synchronous (Single Thread)
python -m src.main --mode sync
# 2. Multi-Threading (Good for I/O bound)
python -m src.main --mode thread
# 3. Multi-Processing (Good for CPU bound)
python -m src.main --mode process
# 4. Asynchronous I/O (Best for high concurrency I/O)
python -m src.main --mode async
```

To collect full experimental data, run the automation script. This will iterate through all combinations of Matrix Sizes (CPU load) and Worker Counts, saving the results to .`experiment_results.csv`

```bash
python run_experiment.py
```

## Configuration

You can adjust the workload characteristics in `src/config.py` to simulate different AI tasks:

* **`MATRIX_SIZE`**: Controls CPU intensity.
* `0`: Pure I/O testing (Disk speed & context switch overhead).
* `200`: Mixed Workload (Realistic preprocessing).
* `500+`: CPU-bound (Stress-testing the GIL).
* **`NUM_WORKERS`**: Number of threads/processes to spawn.
* **`NUM_FILES`**: Total dataset size.