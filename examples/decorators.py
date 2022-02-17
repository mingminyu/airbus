import time
from airbus.decorators import timeit, progressbar

@timeit
def test_timeit():
    for i in range(10):
        time.sleep(1)


@progressbar
def dummy_loop():
    total = 20
    yield total
    
    for i in range(1, total + 1):
        yield i
        time.sleep(1)

    return "done"


f = dummy_loop()
