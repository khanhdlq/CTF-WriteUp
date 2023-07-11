#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/random.h>

void print_func(const char *message) {
    printf("%s", message);
}

void cat_flag()
{
  print_func("YOU WIN. HERE IS YOUR PRIZE:\n");
  system("cat /flag");
  exit(0);
}

unsigned char v2 = 42u;
int main() {

    char v3;

    for (int j = 0; j <= 999; ++j) {       

        if (v2 <= 41u) {
            print_func("... *BAM!*\n-- CONNECTION TERMINATED --\n");
            exit(0);
        }
        
        //print_func("... *click*\n");
        sleep(0.1);
        while(1){
            getrandom(&v2, 1, 0);
            if (v2 >= 42)
            {
                printf("%u", v2);
                break;
            }
        }
        putchar('\n');
        fflush(stdout);
    }
    cat_flag();



    return 0;
}
