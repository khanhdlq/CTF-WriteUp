#include <stdio.h>
#include <stdlib.h>

int main() {
    const char* str = "12345678901234567890";
    long long int num = atoll(str);
    printf("Giá trị của num: %lld\n", num);
    /*_int64 ^ _int64 ^ _int64 = unsigned __int64 */
    return 0;
}