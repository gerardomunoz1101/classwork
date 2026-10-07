#include <stdio.h>

int main(){

    int a = 10;
    int b = 3;
    int c = 5;

    int large1 = 100000;
    int large2 = 100000;

    /*
    Task 1: Operator Precedence
    Add parentheses to the original expression to get 12:
    a + (b * c - a) % b
    */
    int precedence_result = a + b * c - a % b;
    
    printf("%i\n", precedence_result);


    /*
    Task 2: Integer Division
    Kept the data types the same for a and b,
    but casted one of the operands to get required result
    */
    double division_result = (double)a / b;
    printf("%.2f\n", division_result);


    /* 
    Task 3: Large Multiplication
    Used long long type casting on one of the inputs to create a long long output
    */
    long long multiplication_result =(long long) large1 * large2;
    printf("%lld\n", multiplication_result);


    /*
    Task 4: Custom Expression
    
    */
    double custom_expression = (double)(a + c) / b -1;
    printf("%.2f\n", custom_expression);


    return 0;
}
