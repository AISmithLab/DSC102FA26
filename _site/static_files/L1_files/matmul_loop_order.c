/* Matrix multiplication C = A x B, two loop orders, same math.
 *
 *   ijk: inner loop walks B down a column (stride N)   -> cache misses
 *   ikj: inner loop walks B and C along a row (stride 1) -> cache hits
 *
 *   cc -O2 -o matmul matmul_loop_order.c && ./matmul
 */
#include <stdio.h>
#include <time.h>

#define N 1024
static double A[N][N], B[N][N], C[N][N];

static double now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e3 + ts.tv_nsec / 1e6;
}

static void clear(void) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) C[i][j] = 0;
}

int main(void) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) { A[i][j] = i + j; B[i][j] = i - j; }

    clear();
    double t0 = now_ms();
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                C[i][j] += A[i][k] * B[k][j];
    double t_ijk = now_ms() - t0;
    double check1 = C[N / 2][N / 3];

    clear();
    t0 = now_ms();
    for (int i = 0; i < N; i++)
        for (int k = 0; k < N; k++)
            for (int j = 0; j < N; j++)
                C[i][j] += A[i][k] * B[k][j];
    double t_ikj = now_ms() - t0;

    printf("%dx%d double matrix multiply\n", N, N);
    printf("  ijk %8.0f ms\n", t_ijk);
    printf("  ikj %8.0f ms   (%.1fx faster)\n", t_ikj, t_ijk / t_ikj);
    if (check1 != C[N / 2][N / 3]) printf("  results differ!\n");
    return 0;
}
