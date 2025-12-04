import dask.array as da

x = da.random.random((1000, 1000), chunks=(100, 100))
y = x.mean()
print("Dask mean result:", y.compute())


from dask.distributed import Client
import dask.array as da

def main():
    client = Client(processes=False, threads_per_worker=4, n_workers=1, memory_limit='2GB')
    print("Dask client:", client)

    x = da.random.random((10000, 10000), chunks=(1000, 1000))
    print("Dask array x:", x)

    y = x + x.T
    z = y[::2, 5000:].mean(axis=1)
    print("Dask array z (lazy):", z)

    result = z.compute()
    print("Result (numpy array):", result)

    y_persisted = y.persist()
    print("y persisted:", y_persisted)

    first_elem = y_persisted[0, 0].compute()
    total_sum = y_persisted.sum().compute()
    print("First element y[0,0]:", first_elem)
    print("Sum of y:", total_sum)

    client.close()

if '__name__' == '__main__':
    main()
