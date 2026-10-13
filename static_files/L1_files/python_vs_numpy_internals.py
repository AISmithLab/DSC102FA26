"""Why is NumPy faster than pure Python? Measure the pieces.

Companion to copy_demo.py (2048x2048 int64 copy).

Usage:
  python python_vs_numpy_internals.py            # sizes + timings
  python python_vs_numpy_internals.py --only X   # run only one copy (X = setup, py, np_rows, np_full)
                                                 # use with `/usr/bin/time -l` to read
                                                 # "instructions retired" on macOS

Prints:
  1. Memory: a Python int object vs a raw 8-byte value; list-of-ints vs ndarray
  2. Time: pure Python loop, NumPy row loop (2048 calls), NumPy one call (dst[:] = src)
"""

import argparse
import sys
import time

import numpy as np

N = 2048


def best_of(fn, repeats=5):
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


def py_copyij(src, dst, n):
    for i in range(n):
        for j in range(n):
            dst[i * n + j] = src[i * n + j]


def np_copy_rows(src, dst):
    for i in range(src.shape[0]):
        dst[i, :] = src[i, :]


def np_copy_full(src, dst):
    dst[:] = src


def memory():
    print("[Memory]")
    print(f"  sys.getsizeof(1)        = {sys.getsizeof(1)} bytes  (int object header + value)")
    print(f"  sys.getsizeof(10**6)    = {sys.getsizeof(10**6)} bytes")
    print(f"  sys.getsizeof(2**62)    = {sys.getsizeof(2**62)} bytes")
    lst = list(range(N * N))
    ptrs = sys.getsizeof(lst)
    objs = sum(sys.getsizeof(x) for x in lst)
    arr = np.arange(N * N, dtype=np.int64)
    print(f"  list of {N*N:,} ints: {ptrs / 2**20:.0f} MB of pointers + {objs / 2**20:.0f} MB of int objects"
          f" = {(ptrs + objs) / 2**20:.0f} MB")
    print(f"  ndarray int64, same values: {arr.nbytes / 2**20:.0f} MB")
    a2 = arr.reshape(N, N)
    print(f"  ndarray dtype={a2.dtype} shape={a2.shape} strides={a2.strides}")


def timings():
    print(f"\n[Time] {N}x{N} int64, best of several runs")
    from array import array
    src_py = array("q", range(N * N))
    dst_py = array("q", bytes(8 * N * N))
    t_py = best_of(lambda: py_copyij(src_py, dst_py, N), repeats=1)
    src = np.arange(N * N, dtype=np.int64).reshape(N, N)
    dst = np.empty_like(src)
    np_copy_full(src, dst)  # warm up (touch pages)
    t_rows = best_of(lambda: np_copy_rows(src, dst), repeats=20)
    t_full = best_of(lambda: np_copy_full(src, dst), repeats=20)
    small_s, small_d = np.zeros(1, np.int64), np.zeros(1, np.int64)
    t_call = best_of(lambda: [np_copy_full(small_s, small_d) for _ in range(N)], repeats=20) / N
    for name, t in [("pure Python loop", t_py), ("NumPy, 2048 row copies", t_rows),
                    ("NumPy, one call dst[:] = src", t_full)]:
        print(f"  {name:<30} {t * 1e3:8.2f} ms   {t / (N * N) * 1e9:7.2f} ns/element")
    print(f"  overhead of one tiny NumPy copy call: {t_call * 1e9:.0f} ns"
          f"  (x {N} rows = {t_call * N * 1e3:.2f} ms)")


def only(which):
    from array import array
    if which == "py":
        src_py = array("q", range(N * N))
        dst_py = array("q", bytes(8 * N * N))
        py_copyij(src_py, dst_py, N)
    elif which == "setup":
        array("q", range(N * N)); array("q", bytes(8 * N * N))
    else:
        src = np.arange(N * N, dtype=np.int64).reshape(N, N)
        dst = np.empty_like(src)
        (np_copy_rows if which == "np_rows" else np_copy_full)(src, dst)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--only", choices=["setup", "py", "np_rows", "np_full"])
    a = p.parse_args()
    if a.only:
        only(a.only)
    else:
        memory()
        timings()
