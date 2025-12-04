from dask.distributed import Client, as_completed
import time
import random

def task(x):
    time.sleep(random.uniform(0.5, 1.5))
    return x * x

def main():
    client = Client()
    print("Dask cluster:", client)

    inputs = list(range(5))
    futures = [client.submit(task, i) for i in inputs]

    results = []
    for future in as_completed(futures):
        res = future.result()
        print("Done:", res)
        results.append(res)

        if res < 10:
            new_future = client.submit(task, res + 10)
            futures.append(new_future)

    print("All results:", results)

    client.close()

if __name__ == "__main__":
    main()
