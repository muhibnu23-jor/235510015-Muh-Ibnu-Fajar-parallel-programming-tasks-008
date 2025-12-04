from dask.distributed import Client, as_completed
import time
import random

def slow_increment(x):
    time.sleep(random.uniform(0.5, 1.5))
    return x + 1

def slow_add(x, y):
    time.sleep(random.uniform(0.5, 1.5))
    return x + y

def main():
    client = Client(n_workers=2, threads_per_worker=1)
    print("Client:", client)

    futures = []
    for i in range(5):
        fut = client.submit(slow_increment, i)
        futures.append(fut)

    results = client.gather(futures)
    print("Results of slow_increment:", results)

    fut2 = client.submit(slow_add, results[0], results[1])
    print("Result of slow_add:", fut2.result())

    print("Iterating as futures complete:")
    for completed in as_completed(futures):
        res = completed.result()
        print(" - completed:", res)

    client.close()

if __name__ == "__main__":
    main()
