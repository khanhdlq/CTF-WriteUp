#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    setupbuf();
    unsigned int seed = time(0);
    printf("%d\n", seed);
    srand(time(0));
    long int ran_num = rand();
    printf("%d\n", ran_num);
    Time_Freeze();
    long int time_ran = (int)time(0LL);
    printf("%d\n", seed);
    return 0;
}

int Time_Freeze()
{
    printf("Pause time, enter to continue:");
    getchar();
    return printf("\x1B[1A\x1B[K");
}

void setupbuf()
{
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
}