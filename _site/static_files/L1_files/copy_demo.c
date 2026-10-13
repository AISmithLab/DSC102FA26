/* copyij vs. copyji: same work, different memory access order.
 *
 * Copies an N x N matrix of longs (8 bytes) two ways:
 *   copyij -- outer loop over rows i, inner over columns j  (stride-1)
 *   copyji -- outer loop over columns j, inner over rows i  (stride-N)
 *
 * Build and run:
 *   cc -O2 -o copy_demo copy_demo.c
 *   ./copy_demo
 *
 * Change the matrix size at compile time:
 *   cc -O2 -DN=4096 -o copy_demo copy_demo.c
 */

#include <stdio.h>
#include <time.h>

#ifndef N
#define N 2048
#endif

#define REPEATS 5

/* Global arrays: 2 x 2048 x 2048 x 8 bytes = 64 MB, too big for the stack. */
static long src[N][N];
static long dst[N][N];

void copyij(long src[N][N], long dst[N][N]) {
    for (long i = 0; i < N; i++)
        for (long j = 0; j < N; j++)
            dst[i][j] = src[i][j];
}

void copyji(long src[N][N], long dst[N][N]) {
    for (long j = 0; j < N; j++)
        for (long i = 0; i < N; i++)
            dst[i][j] = src[i][j];
}

static double now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e3 + ts.tv_nsec / 1e6;
}

/* Run f a few times and return the fastest time in milliseconds. */
static double best_of(void (*f)(long[N][N], long[N][N])) {
    double best = 1e30;
    for (int r = 0; r < REPEATS; r++) {
        double t0 = now_ms();
        f(src, dst);
        double t = now_ms() - t0;
        if (t < best)
            best = t;
    }
    return best;
}

/* Sum of dst, so the compiler cannot skip the copies. */
static long checksum(void) {
    long s = 0;
    for (long i = 0; i < N; i++)
        for (long j = 0; j < N; j++)
            s += dst[i][j];
    return s;
}

int main(void) {
    for (long i = 0; i < N; i++)
        for (long j = 0; j < N; j++)
            src[i][j] = i * N + j;

    double t_ij = best_of(copyij);
    long sum_ij = checksum();
    double t_ji = best_of(copyji);
    long sum_ji = checksum();

    printf("C, %dx%d long (%zu MB per array)\n", N, N, sizeof(src) >> 20);
    printf("  copyij %9.1f ms\n", t_ij);
    printf("  copyji %9.1f ms   (%.1fx slower)\n", t_ji, t_ji / t_ij);
    if (sum_ij != sum_ji)
        printf("  checksum mismatch!\n");
    return 0;
}
