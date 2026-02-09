import time
import logging

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("OS_Project")

class Timer:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        self.start = time.time()
        logger.info(f"Starting task: {self.name}")
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start
        logger.info(f"Finished {self.name} in {self.duration:.4f} seconds")