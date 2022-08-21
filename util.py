import sys, os, psutil
import subprocess
import time

def profile(func):
    def wrapper(*args, **kwargs):
        pid = os.getpid()
        subprocess.Popen(["./tools/monitor_mem.sh", str(pid)])
        time_before = time.time()
        result = func(*args, **kwargs)
        time_after = time.time()
        print("{}:consumed time:\t{:,}".format(
            func.__name__,
            time_after - time_before))
        return result
    return wrapper
