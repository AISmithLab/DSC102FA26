"""Same copy, smaller numbers: how much does the number format matter?

Copies a 4096 x 4096 array with NumPy (in row-major order, like copyij)
while shrinking the element type: float64 -> float32 -> float16 -> int8.
The number of elements is identical each time; only the bytes per
element change.

Usage:
  python copy_dtype_demo.py            # 4096 x 4096
  python copy_dtype_demo.py --n 4096
"""

import argparse
import time

import numpy as np


def best_of(fn, repeats=9):
    """Run fn a few times and return the fastest wall-clock time in seconds."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4096)
    args = parser.parse_args()
    n = args.n

    rng = np.random.default_rng(0)
    base = rng.standard_normal((n, n))  # float64

    print(f"Copy a {n} x {n} array with NumPy (np.copyto):")
    print(f"  {'dtype':<8} {'bytes/elem':>10} {'array size':>11} {'time':>9} {'speedup':>8} {'GB/s':>6}")
    t_ref = None
    for dtype in (np.float64, np.float32, np.float16, np.int8):
        src = base.astype(dtype)
        dst = np.empty_like(src)

        def copy(src=src, dst=dst):
            np.copyto(dst, src)  # one compiled loop over the whole array

        t = best_of(copy)
        if t_ref is None:
            t_ref = t
        mb = src.nbytes / 1e6
        gbs = 2 * src.nbytes / t / 1e9  # read + write
        print(f"  {np.dtype(dtype).name:<8} {src.itemsize:>10} {mb:>8.0f} MB {t * 1e3:>7.2f} ms {t_ref / t:>7.1f}x {gbs:>6.0f}")


if __name__ == "__main__":
    main()
