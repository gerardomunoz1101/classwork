#include <limits.h>
#include <stdio.h>

int main(void) {
    // Task 1: Declare one variable of each required type
    char u = 'u';
    short m = 100;
    int i = 22;
    long l = 100000L;
    long long ll = 10000000000LL;
    unsigned int ui = 400000000U;
    float f = 3.14f;
    double d = 3.14159;

    // Task 2: Print the value and size each variable
    printf("Type: Char | Value: '%c' | Size: %zu bytes\n", u, sizeof(u));
    printf("Type: Short | Value: '%hd' | Size: %zu bytes\n", m, sizeof(m));
    printf("Type: Int | Value: '%d' | Size: %zu bytes\n", i, sizeof(i));
    printf("Type: Long | Value: '%ld' | Size: %zu bytes\n", l, sizeof(l));
    printf("Type: Long Long | Value: '%lld' | Size: %zu bytes\n", ll, sizeof(ll));
    printf("Type: Unsigned Int | Value: '%u' | Size: %zu bytes\n", ui, sizeof(ui));
    printf("Type: Float | Value: '%f' | Size: %zu bytes\n", f, sizeof(f));
    printf("Type: Double | Value: '%f' | Size: %zu bytes\n", d, sizeof(d));

    // Task 3: Print the minimum and maximum int values
    printf("Minimum int value: %d\n", INT_MIN);
    printf("Maximum int value: %d\n", INT_MAX);

    return 0;
}


