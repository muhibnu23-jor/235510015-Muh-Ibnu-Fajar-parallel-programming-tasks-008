# prefect_dask_etl.py

from prefect import flow, task
from dask.distributed import Client
import dask.dataframe as dd

@task
def load_data(path_pattern):
    # baca file CSV (bisa banyak file) dengan Dask DataFrame
    df = dd.read_csv(path_pattern, assume_missing=True)
    return df

@task
def clean_data(df):
    # contoh cleaning sederhana — drop baris dengan nilai NA
    df2 = df.dropna()
    return df2

@task
def aggregate_data(df):
    # contoh agregasi: hitung rata-rata kolom numeric 'value', per kategori di 'category'
    result = df.groupby("category").value.mean().compute()
    return result

@task
def save_result(result, out_path):
    # simpan hasil agregasi ke file teks
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(str(result))

@flow
def etl_flow(path_pattern, out_path):
    df = load_data(path_pattern)
    df_clean = clean_data(df)
    summary = aggregate_data(df_clean)
    save_result(summary, out_path)
    return summary

if __name__ == "__main__":
    # Mulai Dask cluster lokal
    client = Client()
    print("Dask Cluster:", client)

    # Contoh: jalankan flow ETL pada semua CSV di folder 'data/'
    summary = etl_flow("data/*.csv", "result_summary.txt")
    print("ETL selesai. Summary:", summary)
