#include <stdio.h>

int main() {
    char s[256];  // Adjust the size as needed
    char a[] = "aaaaa";
    char b[] = "bbbb;ls && ls -la";

    // Create and format the command
    sprintf(s, "echo \"%s\"\\n%s\" > data/advice", a, b);

    // Print the formatted command
    printf("%s\n", s);

    return 0;
}
