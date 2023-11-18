#include <stdio.h>
#include <stdlib.h>

int main()
{
    char s[100];
    FILE *fd = fopen("flag","r");
    fgets(s, 100, fd);
    printf("%s\n", s);
    fclose(fd);
    return 0;
}