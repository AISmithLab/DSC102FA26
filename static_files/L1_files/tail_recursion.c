/* Tail recursion: what an optimizing compiler does with a tail call.
 *
 *   cc -O0 -o tail tail_recursion.c && ./tail   # crashes: 100 M stack frames
 *   cc -O2 -o tail tail_recursion.c && ./tail   # prints the answer instantly
 *   cc -O2 -S -o - tail_recursion.c             # gcd: a loop, no call
 *                                               # sum_to: replaced by n(n+1)/2
 */
#include <stdio.h>

long gcd(long a, long b) {
    if (b == 0) return a;
    return gcd(b, a % b);           /* tail call */
}

long sum_to(long n, long acc) {
    if (n == 0) return acc;
    return sum_to(n - 1, acc + n);  /* tail call */
}

int main(void) {
    printf("gcd(1071, 462) = %ld\n", gcd(1071, 462));
    printf("sum_to(100000000) = %ld\n", sum_to(100000000, 0));
    return 0;
}
