from dask.distributed import Client
import dask
import dask.dataframe as dd

def main():
    client = Client(n_workers=2, threads_per_worker=2, memory_limit="1GB")
    print(client)

    df = dask.datasets.timeseries()

    print("Dtypes:\n", df.dtypes)
    print(df.head(3))

    df2 = df[df.y > 0]
    df3 = df2.groupby("name").x.std()
    print("Series (belum dihitung):", df3)

    computed = df3.compute()
    print("Hasil compute():\n", computed)

    df4 = df.groupby("name").aggregate({"x": "sum", "y": "max"})
    res4 = df4.compute()
    print("Hasil aggregasi sum x, max y per name:\n", res4)

    df4_small = df4.repartition(npartitions=1)
    joined = df.merge(df4_small, left_on="name", right_index=True,
                      suffixes=("_original", "_aggregated"))
    print(joined.head())

    df = df.persist()
    print("Persisted:", df)

    resampled = df[["x", "y"]].resample("1h").mean()
    print(resampled.head())


if __name__ == "__main__":
    main()
