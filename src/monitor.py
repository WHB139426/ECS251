import psutil
import os
import time
from threading import Thread

class ResourceMonitor:
    """
    监控进程及所有子进程的资源使用情况（内存RSS, 上下文切换）
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.keep_running = False
        self.peak_rss = 0
        self.ctx_switches_start = 0
        self.ctx_switches_end = 0

    def _get_total_ctx(self):
        """计算主进程加上所有子进程的上下文切换总和"""
        try:
            ctx = self.process.num_ctx_switches()
            total = ctx.voluntary + ctx.involuntary
            for child in self.process.children(recursive=True):
                c_ctx = child.num_ctx_switches()
                total += c_ctx.voluntary + c_ctx.involuntary
            return total
        except (psutil.NoSuchProcess, PermissionError):
            return 0

    def _get_total_memory(self):
        """计算主进程加上所有子进程的当前物理内存使用量 (RSS)"""
        try:
            mem = self.process.memory_info().rss
            for child in self.process.children(recursive=True):
                mem += child.memory_info().rss
            return mem
        except (psutil.NoSuchProcess, PermissionError):
            return 0

    def _monitor_loop(self):
        while self.keep_running:
            mem = self._get_total_memory()
            if mem > self.peak_rss:
                self.peak_rss = mem
            time.sleep(0.01)  # 10ms 采样一次

    def __enter__(self):
        self.ctx_switches_start = self._get_total_ctx()
        self.keep_running = True
        self.peak_rss = self._get_total_memory()
        self.monitor_thread = Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.keep_running = False
        self.monitor_thread.join()
        self.ctx_switches_end = self._get_total_ctx()
        
        # 计算差值与转换单位
        self.total_ctx_switches = self.ctx_switches_end - self.ctx_switches_start
        self.peak_memory_mb = self.peak_rss / (1024 * 1024)