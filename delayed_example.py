from dask import delayed
import time

def inc(x):
    time.sleep(1)
    return x + 1

def double(x):
    time.sleep(1)
    return x * 2

def add(x, y):
    time.sleep(1)
    return x + y

if __name__ == "__main__":

    a = delayed(inc)(10)
    b = delayed(double)(a)
    c = delayed(add)(a, b)

    print("Computing...")
    result = c.compute()

    print("Result:", result)
