import json
import requests
from dask import delayed, compute

@delayed
def fetch(url):
    print(f"Mengambil data dari: {url}")
    r = requests.get(url)
    return r.json()

urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3",
]

tasks = [fetch(u) for u in urls]

results = compute(*tasks)

print("\nHasil JSON yang diterima:")
for r in results:
    print(r)
