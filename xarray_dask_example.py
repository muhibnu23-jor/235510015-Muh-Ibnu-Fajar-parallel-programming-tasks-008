import xarray as xr
import dask.array as da
import pandas as pd

def main():
    times = pd.date_range("2000-01-01", periods=365, freq="D")
    x = range(100)
    y = range(50)

    data = da.random.random(
        size=(len(times), len(x), len(y)),
        chunks=(50, 100, 50)
    )

    ds = xr.Dataset(
        {"var": (("time", "x", "y"), data)},
        coords={
            "time": times,
            "x": x,
            "y": y
        }
    )

    print("Dataset XArray (lazy, dask-backed):")
    print(ds)

    mean_time = ds["var"].mean(dim=("x", "y"))

    print("\nLazy mean over x & y (per time):")
    print(mean_time)

    result = mean_time.compute()
    print("\nHasil compute():")
    print(result)

    result.to_netcdf("mean_time.nc")
    print("\nHasil disimpan ke mean_time.nc")

if __name__ == "__main__":
    main()
