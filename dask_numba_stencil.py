import dask.array as da
from numba import jit
import numpy as np

@jit(nopython=True)
def stencil_step(a):
    n, m = a.shape
    b = np.empty_like(a)
    for i in range(1, n-1):
        for j in range(1, m-1):
            b[i, j] = 0.2*(a[i, j] + a[i-1,j] + a[i+1,j] + a[i,j-1] + a[i,j+1])
    return b

def main():
    x = da.random.random((1000, 1000), chunks=(250, 250))

    y = x.map_blocks(lambda block: stencil_step(block), dtype=float)

    result = y.compute()

    print("Processed array shape:", result.shape)
    print("Contoh nilai di tengah:", result[result.shape[0]//2, result.shape[1]//2])

if __name__ == "__main__":
    main()
