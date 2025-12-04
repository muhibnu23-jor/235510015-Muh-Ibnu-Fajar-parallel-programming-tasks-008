import asyncio
from dask.distributed import Client
from dask import delayed

def square(x):
    return x * x

@delayed
def delayed_square(x):
    return square(x)

async def main():
    print("Dask Cluster running...")
    client = Client(processes=True, n_workers=2, threads_per_worker=1)
    print(client)

    print("Menghitung secara asynchronous ...")

    tasks = [delayed_square(i) for i in range(10)]

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        None,
        lambda: client.gather(client.compute(tasks))
    )

    print("Hasil perhitungan:", result)

    client.close()  

if __name__ == "__main__":
    asyncio.run(main())
