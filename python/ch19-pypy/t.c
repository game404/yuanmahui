#include <stdio.h>
#include <time.h>

const long long TOTAL = 100000000;

long long mySum()
{
    long long number=0;
    long long i;
    for( i = 0; i < TOTAL; i++ )
    {
        number += i;
    }
    return number;
}


int main(void)
{
    // Start measuring time
    clock_t start = clock();

    printf("%llu \n", mySum());
    // Stop measuring time and calculate the elapsed time
    clock_t end = clock();
    double elapsed = (end - start)/CLOCKS_PER_SEC;
    printf("Time measured: %.3f seconds.\n", elapsed);
    return 0;
}
