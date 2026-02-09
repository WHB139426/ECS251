import os
import random
from src.utils import logger
from src import config

def generate_dataset():
    # 使用 config.DATA_DIR 代替 "./data"
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)
        logger.info(f"Created directory: {config.DATA_DIR}")
    
    logger.info(f"Generating {config.NUM_FILES} files...") # 使用 config 里的数量
    
    for i in range(config.NUM_FILES):
        # 使用 config 里的范围
        size_mb = random.randint(config.MIN_FILE_SIZE_MB, config.MAX_FILE_SIZE_MB)
        file_path = os.path.join(config.DATA_DIR, f"file_{i:03d}_{size_mb}MB.bin")
        
        with open(file_path, "wb") as f:
            f.write(os.urandom(size_mb * 1024 * 1024))
            
    logger.info("Data generation complete.")

if __name__ == "__main__":
    generate_dataset()