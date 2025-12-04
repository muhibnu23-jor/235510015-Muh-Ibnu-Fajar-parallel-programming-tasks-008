import pandas as pd
import dask.dataframe as dd
from dask.distributed import Client
from prophet import Prophet
import matplotlib.pyplot as plt

def main():
    client = Client()
    print("Dask Client:", client)

    dates = pd.date_range(start='2020-01-01', periods=365, freq='D')
    y = (pd.Series(10 + 5 * np.sin(2 * np.pi * dates.dayofyear / 365) +
                   np.random.randn(len(dates)), index=dates)).values

    df = pd.DataFrame({'ds': dates, 'y': y})
    print("Sample data (pandas):")
    print(df.head())

    ddf = dd.from_pandas(df, npartitions=4)
    df_clean = ddf.compute()

    m = Prophet()
    m.fit(df_clean)

    future = m.make_future_dataframe(periods=30)  
    forecast = m.predict(future)

    print("\nForecast head:")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

    fig = m.plot(forecast)
    plt.show()

if __name__ == "__main__":
    import numpy as np
    main()
