import threading
import subprocess
from time import perf_counter, sleep
import tracemalloc


class Runner(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        self.time = None
        self.memory = None
        self.peakmemory = None
        threading.Thread.__init__(self)

    def run(self,code: str):
        s = perf_counter()
        p = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        cu, peak = tracemalloc.get_traced_memory()
        e = perf_counter()
        self.stdout, self.stderr = p.communicate()
        self.stdout = self.stdout.decode("utf-8")
        self.stderr = self.stderr.decode("utf-8")
        self.time = str(e - s)
        self.memory = cu
        self.peakmemory = peak

