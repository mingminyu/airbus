import time
from airbus.decorators import timeit, progressbar, retry


@retry(retry_times=2, sleep_time=3)
def retry_func():
    print(1 / 0)


retry_func()