#include <stdio.h>
#include <time.h>

int main()
{
    int v3 = time(0LL);
    srand(v3);
    int v[10];

    for ( int i = 0; i <= 9; ++i )
        v[i] = rand();
    for ( int i = 0; i <= 9; ++i )
        printf("%d\n", v[i]);
}