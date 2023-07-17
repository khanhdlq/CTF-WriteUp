#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
int global_canary;
int generate_canary()
{
  unsigned int v0; // eax
  int result; // eax

  v0 = time(0LL);
  srand(v0);
  result = rand();
  global_canary = result;
  return result;
}
int main ()
{
    unsigned int v3; // eax
    generate_canary();
    printf("%d\n", global_canary);
    v3 = rand();
    printf("%d\n", v3);
}