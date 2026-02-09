import os
import random
from src.utils import logger

DATA_DIR = "./data"
NUM_FILES = 50
MIN_SIZE_MB = 1
MAX_SIZE_MB = 10

def generate_dataset():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.info(f"Created directory: {DATA_DIR}")
    
    logger.info(f"Generating {NUM_FILES} files with random sizes ({MIN_SIZE_MB}-{MAX_SIZE_MB}MB)...")
    
    for i in range(NUM_FILES):
        # Random size for each file
        size_mb = random.randint(MIN_SIZE_MB, MAX_SIZE_MB)
        file_path = os.path.join(DATA_DIR, f"file_{i:03d}_{size_mb}MB.bin")
        
        # Write random bytes
        with open(file_path, "wb") as f:
            f.write(os.urandom(size_mb * 1024 * 1024))
            
    logger.info("Data generation complete.")

if __name__ == "__main__":
    generate_dataset()