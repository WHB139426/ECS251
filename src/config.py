import os

# ================= PROJECT PATHS =================
# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory where synthetic data will be stored
DATA_DIR = os.path.join(BASE_DIR, "data")

# Directory for logs and results
LOG_DIR = os.path.join(BASE_DIR, "logs")
RESULTS_FILE = os.path.join(LOG_DIR, "benchmark_results.csv")


# ================= DATA GENERATION SETTINGS =================
# Total number of files to generate for the dataset
NUM_FILES = 100

# File size range in MB (Simulating variable video chunk sizes)
# 1MB = small image, 10MB = 4K video frame
MIN_FILE_SIZE_MB = 1
MAX_FILE_SIZE_MB = 10


# ================= BENCHMARK SETTINGS =================
# Number of worker threads/processes to spawn
# Usually set to number of CPU cores (e.g., 4, 8, 16)
NUM_WORKERS = 4

# Matrix size for CPU workload simulation (N x N multiplication)
#   - 0   : Pure IO-bound (Testing disk speed & context switch overhead)
#   - 200 : Mixed Workload (Realistic preprocessing)
#   - 1000: CPU-bound (Testing parallel compute capability)
MATRIX_SIZE = 200

# Random seed for reproducibility
RANDOM_SEED = 42