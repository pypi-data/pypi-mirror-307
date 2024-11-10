import os
import psutil

def virtualmem() -> dict[str, float]:
    total = psutil.virtual_memory().total / (1024 ** 3)
    available = psutil.virtual_memory().available / (1024 ** 3)
    used = psutil.virtual_memory().used / (1024 ** 3)
    recommended_maximum = total / 4

    return {
        'total': total,
        'recommended_maximum': recommended_maximum,
        'available': available,
        'used': used,
    }

class VirtualMemory:
    def __init__(self) -> None:
        self.system = virtualmem()
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.memory_info = self.process.memory_info()
        self.used = self.system["used"]
        self.rss = self.memory_info.rss / (1024 ** 2) - self.used

    def __float__(self) -> float:
        return self.system["recommended_maximum"]

    def __call__(self) -> 'VirtualMemory':
        self.system = virtualmem()
        self.memory_info = self.process.memory_info()
        self.rss = self.memory_info.rss / (1024 ** 2) - self.used
        return self

class VirMemProcess:
    def __init__(self) -> None:
        self.available: bool = False
        self.double: bool = False
        self.maximum: bool = False
        self.usage: bool = False
        self.virmem = VirtualMemory()
        self.system = self.virmem.system

    def __call__(
        self,
        *,
        available: bool = False,
        double: bool = False,
        maximum: bool = False,
        usage: bool = False) -> None:
        self.available: bool = available
        self.double: bool = double
        self.maximum: bool = maximum
        self.usage: bool = usage
        self.virmem = VirtualMemory()
        return self

    def __enter__(self):
        self.virmem()

        if self.available:
            self.system["recommended_maximum"] = self.system["available"]
        if self.double:
            self.system["recommended_maximum"] *= 2
        if self.maximum:
            self.system["recommended_maximum"] = self.system["total"]
        if self.usage:
            print(f'System Used: {self.system["used"]:.2f}gb')
            print(f'System Available: {self.system["available"]:.2f}gb')
            print(f'System Total: {self.system["total"]:.2f}gb')
            print(f'Recommended Maximum: {self.system["recommended_maximum"]:.2f}gb')
            print(f'Process Used: {self.virmem.rss / 2:.2f}gb')
        if float(self.virmem) > self.virmem.rss / 2:
            return self
        raise MemoryError('Context manager not allowed due to insufficient available memory')

    def __exit__(self, type, value, traceback):
        pass

vmprocess = VirMemProcess()
__version__ = 'v1.0.0'


__all__ = [
    "vmprocess",
    "__version__"]
