/* How long does one memory access take? Depends on how much data you touch.
 *
 * Pointer chasing: each load's address comes from the previous load, so the CPU
 * cannot overlap or prefetch them. Time per load ≈ latency of wherever the data lives
 * (L1, L2, ..., DRAM). The chain is a random cycle through the whole buffer.
 *
 *   cc -O2 -o memory_latency memory_latency.c && ./memory_latency
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}

int main(void) {
    printf("%10s %12s\n", "size", "ns/access");
    for (size_t bytes = 16 << 10; bytes <= (size_t)1 << 30; bytes *= 2) {
        size_t n = bytes / sizeof(void *);
        void **buf = malloc(n * sizeof(void *));
        size_t *order = malloc(n * sizeof(size_t));
        for (size_t i = 0; i < n; i++) order[i] = i;
        srand(1);
        for (size_t i = n - 1; i > 0; i--) {          /* random permutation */
            size_t j = ((size_t)rand() * RAND_MAX + rand()) % (i + 1);
            size_t t = order[i]; order[i] = order[j]; order[j] = t;
        }
        for (size_t i = 0; i < n; i++)                 /* one big random cycle */
            buf[order[i]] = &buf[order[(i + 1) % n]];
        free(order);

        size_t steps = 20 * 1000 * 1000;
        void **p = (void **)buf[0];
        for (size_t i = 0; i < n; i++) p = (void **)*p;   /* warm up */
        double t0 = now_ns();
        for (size_t i = 0; i < steps; i++) p = (void **)*p;
        double ns = (now_ns() - t0) / steps;
        if (p == NULL) printf("!");                     /* keep the loop alive */

        if (bytes < (1 << 20)) printf("%7zu KB %12.2f\n", bytes >> 10, ns);
        else                   printf("%7zu MB %12.2f\n", bytes >> 20, ns);
        free(buf);
    }
    return 0;
}
