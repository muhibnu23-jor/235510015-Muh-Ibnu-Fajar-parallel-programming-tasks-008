from dask.distributed import Client
import time
import random

def slow_task(x):
    time.sleep(random.uniform(0.5, 1.5))
    return x * x

def main():
    client = Client()
    print("Dask Cluster:", client)

    inputs = list(range(10))  
    print("Inputs:", inputs)

    futures = [client.submit(slow_task, x) for x in inputs]

    results = client.gather(futures)

    print("Results:", results)

    client.close()

if __name__ == "__main__":
    main()
