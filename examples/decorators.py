import time
from airbus.decorators import timeit, progressbar, retry

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

@retry(retry_times=2, sleep_time=3)
def retry_func():
    print(1 / 0)


# f = dummy_loop()
# retry_func()




class Test(object):
    e = 2
    f = 2

    def __init__(self, a=1, b=2, c=3, d=4):
        self.c = c
        self.d = d
        Test.e = a
        Test.f = b

        # print(e, f)
        print(a, b, self.c, self.d)
    
    @retry(retry_times=e, sleep_time=f)
    def t1(self):
        print(1 / 0)

t = Test(a=3, b=10)
print(t.t1())

