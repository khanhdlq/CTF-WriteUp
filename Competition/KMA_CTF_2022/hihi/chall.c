#include<stdio.h>
#include<string.h>
#include<stdlib.h>
void success(){
    // asm("movq $0x0, %rbp\n\t"
    //     "movq %rbp, %rsp");
    puts("Well!! Next challenge >>>");
    system("cat flag.txt");
}

void vuln(){
    char buffer[32];
    memset(buffer, 0, sizeof(buffer));
    printf("########################\n");
    printf("#                      #\n");
    printf("#         bank         #\n");
    printf("#                      #\n");
    printf("**\n\n");
    printf("Give me your name to login: \n");
    gets(&buffer);
    puts("Thank you!!");
}
int main()
{
    vuln();
    return 0;
}