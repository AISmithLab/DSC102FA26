"""copyij vs. copyji: same work, different memory access order.

Copies an N x N matrix of 8-byte integers two ways:
  copyij  -- outer loop over rows i, inner over columns j  (stride-1, row by row)
  copyji  -- outer loop over columns j, inner over rows i  (stride-N, column by column)

Both do exactly N*N copies. The only difference is the order of memory accesses.

Usage:
  python copy_demo.py                 # run all parts
  python copy_demo.py --part 1        # just one part
  python copy_demo.py --n 4096        # change matrix size

Parts:
  1. Pure Python on a flat row-major buffer (like a C 2D array)
  2. NumPy, same two loop orders
  3. NumPy with column-major (Fortran) layout: the winner flips
  4. Size sweep: the gap appears once the matrix no longer fits in cache
"""

import argparse
import time
from array import array


def best_of(fn, repeats=3):
    """Run fn a few times and return the fastest wall-clock time in seconds."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times)


def report(name_a, t_a, name_b, t_b):
    print(f"  {name_a:<8} {t_a * 1e3:9.1f} ms")
    print(f"  {name_b:<8} {t_b * 1e3:9.1f} ms   ({t_b / t_a:.1f}x slower)" if t_b >= t_a
          else f"  {name_b:<8} {t_b * 1e3:9.1f} ms   ({t_a / t_b:.1f}x faster)")


# ---------------------------------------------------------------------------
# Part 1: pure Python. src/dst are flat buffers; element (i, j) lives at i*n + j,
# exactly how C lays out long src[N][N].
# ---------------------------------------------------------------------------

def py_copyij(src, dst, n):
    for i in range(n):
        for j in range(n):
            dst[i * n + j] = src[i * n + j]


def py_copyji(src, dst, n):
    for j in range(n):
        for i in range(n):
            dst[i * n + j] = src[i * n + j]


def part1(n):
    print(f"\n[Part 1] Pure Python, {n}x{n} int64, row-major buffer")
    src = array("q", range(n * n))
    dst = array("q", bytes(8 * n * n))
    t_ij = best_of(lambda: py_copyij(src, dst, n), repeats=1)
    t_ji = best_of(lambda: py_copyji(src, dst, n), repeats=1)
    report("copyij", t_ij, "copyji", t_ji)
    print("  -> Gap is small: interpreter overhead per element hides the memory cost.")


# ---------------------------------------------------------------------------
# Part 2/3: NumPy. Each Python-level step copies one whole row or one whole column,
# so the interpreter overhead is identical and memory access order dominates.
# ---------------------------------------------------------------------------

def np_copyij(src, dst):
    for i in range(src.shape[0]):
        dst[i, :] = src[i, :]      # one row: contiguous in row-major


def np_copyji(src, dst):
    for j in range(src.shape[1]):
        dst[:, j] = src[:, j]      # one column: every element N*8 bytes apart


def part2(np, n):
    print(f"\n[Part 2] NumPy, {n}x{n} int64, row-major (C order)")
    src = np.arange(n * n, dtype=np.int64).reshape(n, n)
    dst = np.empty_like(src)
    print(f"  strides = {src.strides}  (bytes to next row, next column)")
    t_ij = best_of(lambda: np_copyij(src, dst))
    t_ji = best_of(lambda: np_copyji(src, dst))
    report("copyij", t_ij, "copyji", t_ji)
    assert np.array_equal(src, dst)


def part3(np, n):
    print(f"\n[Part 3] NumPy, {n}x{n} int64, column-major (Fortran order)")
    src = np.asfortranarray(np.arange(n * n, dtype=np.int64).reshape(n, n))
    dst = np.empty_like(src, order="F")
    print(f"  strides = {src.strides}  (bytes to next row, next column)")
    t_ij = best_of(lambda: np_copyij(src, dst))
    t_ji = best_of(lambda: np_copyji(src, dst))
    report("copyij", t_ij, "copyji", t_ji)
    print("  -> Same code, different layout: now copyji is the fast one.")


def part4(np):
    print("\n[Part 4] Size sweep, NumPy row-major, time per element")
    print(f"  {'N':>6} {'matrix':>9} {'copyij':>10} {'copyji':>10} {'ratio':>6}")
    for n in [64, 128, 256, 512, 1024, 2048, 4096]:
        src = np.arange(n * n, dtype=np.int64).reshape(n, n)
        dst = np.empty_like(src)
        repeats = max(3, 2_000_000 // (n * n))
        t_ij = best_of(lambda: np_copyij(src, dst), repeats) / (n * n)
        t_ji = best_of(lambda: np_copyji(src, dst), repeats) / (n * n)
        size = src.nbytes
        size_str = f"{size / 2**20:.0f} MB" if size >= 2**20 else f"{size / 2**10:.0f} KB"
        print(f"  {n:>6} {size_str:>9} {t_ij * 1e9:>7.2f} ns {t_ji * 1e9:>7.2f} ns {t_ji / t_ij:>5.1f}x")
    print("  -> Small matrices fit in cache, so order barely matters; large ones do not.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=2048, help="matrix size N (default 2048)")
    parser.add_argument("--part", type=int, choices=[1, 2, 3, 4], help="run only this part")
    args = parser.parse_args()

    parts = [args.part] if args.part else [1, 2, 3, 4]
    if 1 in parts:
        part1(args.n)
    if any(p in parts for p in (2, 3, 4)):
        import numpy as np
        if 2 in parts:
            part2(np, args.n)
        if 3 in parts:
            part3(np, args.n)
        if 4 in parts:
            part4(np)


if __name__ == "__main__":
    main()
