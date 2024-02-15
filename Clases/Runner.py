import threading
import subprocess
from time import perf_counter, sleep
import tracemalloc
from threading import Timer

class Runner(threading.Thread):
    def __init__(self):
        self.stdout = ''
        self.stderr = 'Tiempo de ejecución excedido'
        self.time = None
        self.memory = None
        self.peakmemory = None
        threading.Thread.__init__(self)

    def run(self,code: str,timeout: int=3):
        s = perf_counter()
        p = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        timer = Timer(timeout, p.kill)
        try:
            timer.start()
            self.stdout, self.stderr = p.communicate()
            self.stdout = self.stdout.decode("utf-8")
            self.stderr = self.stderr.decode("utf-8")
        finally:
            print("Proceso terminado")
            self.stderr = "Tiempo de ejecución excedido"
            self.stdout = ""
            timer.cancel()
        cu, peak = tracemalloc.get_traced_memory()
        e = perf_counter()
        self.time = str(e - s)
        self.memory = cu
        self.peakmemory = peak


