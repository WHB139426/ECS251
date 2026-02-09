from abc import ABC, abstractmethod
from typing import List, Dict

class DataLoader(ABC):
    """
    Abstract Base Class that defines the interface for all concurrency models.
    """
    def __init__(self, data_dir: str, matrix_size: int):
        self.data_dir = data_dir
        self.matrix_size = matrix_size
        self.results: Dict = {}

    @abstractmethod
    def load_and_process(self, files: List[str]) -> float:
        """
        Must return the total time taken (in seconds).
        """
        pass

    def cpu_bound_task(self):
        """
        Simulates the heavy matrix multiplication task.
        """
        import numpy as np
        if self.matrix_size > 0:
            a = np.random.rand(self.matrix_size, self.matrix_size)
            b = np.random.rand(self.matrix_size, self.matrix_size)
            np.dot(a, b)