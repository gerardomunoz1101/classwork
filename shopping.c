#include <stdio.h>
#include <stdarg.h>

void applyTax(double price) {
    price = price * 1.07;
    printf("Inside applyTax(): $%.2f\n", price);
}

void applyDiscount(double *price, double discount) {
    *price = *price - (*price * discount / 100.0);
}

double calculateTotal(int count, ...) {
    va_list args;
    double total = 0.0;

    va_start(args, count);

    for (int i = 0; i < count; i++) {
        total += va_arg(args, double);
    }

    va_end(args);

    return total;
}

int main(void) {
    double price = 100.00;

    printf("---Part 1: Pass by Value ---\n");
    printf("Before applyTax(): $%.2f\n", price);
    applyTax(price);
    printf("After applyTax(): $%.2f\n\n", price);

    printf("--- Part 2: Pass by Reference ---\n");
    printf("Before applyDiscount(): $%.2f\n", price);
    applyDiscount(&price, 20.0);
    printf("After applyDiscount(): $%.2f\n\n", price);

    printf("--- Part 3: Variable Argument Lists ---\n");
    double total1 = calculateTotal(3, 10.00, 20.00, 30.00);
    double total2 = calculateTotal(5, 5.00, 10.00, 15.00, 20.00, 25.00);
    printf("Total of 3 items: $%.2f\n", total1);
    printf("Total of 5 items: $%.2f\n", total2);

    return 0;

}

