import dask.bag as db
import json

def main():
   
    data = [
        {"name": "Alice", "age": 25, "occupation": "Engineer"},
        {"name": "Bob", "age": 40, "occupation": "Doctor"},
        {"name": "Charlie", "age": 35, "occupation": "Engineer"},
        {"name": "Diana", "age": 28, "occupation": "Teacher"},
        {"name": "Eve", "age": 45, "occupation": "Doctor"},
    ]

    with open("people.json", "w", encoding="utf-8") as f:
        for rec in data:
            f.write(json.dumps(rec) + "\n")

    b = db.read_text("people.json").map(json.loads)

    print("All records:", b.compute())

    b2 = b.filter(lambda rec: rec.get("age", 0) > 30)
    print("Filtered (age > 30):", b2.compute())

    occup = b2.map(lambda rec: rec.get("occupation"))
    print("Occupations:", occup.compute())

    freq = occup.frequencies()
    print("Frequencies:", freq.compute())

    top = freq.topk(5, key=lambda x: x[1])
    print("Top occupations:", top.compute())


if __name__ == "__main__":
    main()
