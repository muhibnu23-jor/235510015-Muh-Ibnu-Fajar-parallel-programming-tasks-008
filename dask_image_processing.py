import os
from dask import delayed, compute
from PIL import Image

def process_image(path, out_folder, size=(256, 256)):
    img = Image.open(path)
    img = img.resize(size)
    arr = img.convert("L") 
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    out_path = os.path.join(out_folder, name + "_gray.png")
    arr.save(out_path)
    return out_path

def main():
    input_folder = "images"
    output_folder = "processed"
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.isdir(input_folder):
        print("Folder input tidak ditemukan:", input_folder)
        return

    paths = [os.path.join(input_folder, f)
             for f in os.listdir(input_folder)
             if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))]

    if not paths:
        print("Tidak ada gambar di folder:", input_folder)
        return

    print("Found images:", paths)

    tasks = [delayed(process_image)(p, output_folder) for p in paths]

    results = compute(*tasks)
    print("Processed images:", results)

if __name__ == "__main__":
    main()
