#include <stdio.h>

int main(void)
{
    int number;

    printf("Enter an integer: ");

    /* Read the number and verify that input succeeds. */

    /*
    * Test the number and print:
    
    * FizzBuzz, Fizz, Buzz, or the number.
    */
    if (scanf("%d", &number) != 1) {
        printf("Error: please enter a valid integer.\n");
        return 1;
    }

    if (number % 3 == 0 && number % 5 == 0) {
        printf("Fizzbuzz\n");
    } else if (number % 3 == 0) {
        printf("Fizz\n");
    } else if (number % 5 == 0) {
        printf("Buzz\n");
    } else {
        printf("%d\n", number);
    }

    return 0;

}
