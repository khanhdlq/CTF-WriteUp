#include <stdio.h>
#include <stdlib.h>
int part1 = 0;
int part2 = 0;

int custom_putchar(int value) {
    putchar(value);
    return value;
}

int FUN_00101160(int a1, int a2, int a3, int a4, int a5, int a6, int a7) {
    int result;

    if (!part1) {
        custom_putchar(a7 | a6 | a3 | (char)a2);
        custom_putchar(a7 | a6 | a4 | (char)a3);
        custom_putchar(a7 | a6 | a1);
        custom_putchar(a7 | a6 | a3 | a2 | a1);
        custom_putchar(a7 | a6 | a5 | a4 | a2 | a1);
        part1 = 1;
    }

    if (part1) {
        custom_putchar(a7 | a6 | a5 | a3 | a2 | a1);
        custom_putchar(a7 | a6 | (char)a4);
        custom_putchar(a7 | a6 | a1);
        custom_putchar(a7 | a6 | a5 | (char)a3);
        custom_putchar(a7 | a5 | a4 | a3 | a2 | a1);
        custom_putchar(a7 | a6 | a1);
        custom_putchar(a7 | a5 | a4 | a3 | a2 | a1);
        custom_putchar(a7 | a6 | a4 | a3 | a1);
        custom_putchar(a7 | a6 | a3 | a1);
        custom_putchar(a7 | a6 | a5 | a2 | a1);
        custom_putchar(a7 | a6 | a5 | a2 | a1);
        part2 = 1;
    }

    result = part2;
    if (part2) {
        custom_putchar(a7 | a6 | a5 | a4 | a3 | a1);
        return custom_putchar(a4 | (char)a2);
    }

    return result;
}


int main(){
    int v27 = 0;
    int v26, v25, v24, v23, v22, v21, v20, v19;
    v26 = 0x1010101;
    v25 = 33686018;
    v24 = 67372036;
    v23 = 134744072;
    v22 = 269488144;
    v21 = 538976288;
    v20 = 1077952576;
    v19 = -2139062144;

    FUN_00101160(v26, v25, v24, v23, v22, v21, v20);
}