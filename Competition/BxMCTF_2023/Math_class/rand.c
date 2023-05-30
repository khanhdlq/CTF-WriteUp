#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));
    int lim = rand() % 8192;
    for (int i = 0; i < lim; i++) {
        rand();
    }
    
    for (int i = 0, a, b, c; i < 5; i++) {
        a = rand(); b = rand();
    }
    for (int i = 0, a, b, c; i < 5; i++) {
        b = rand(); c = rand();
        printf("%d = %d \n", b, c);
        }
}
