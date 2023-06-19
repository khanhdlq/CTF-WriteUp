#include <stdio.h>
#include <stdlib.h>

// gcc -no-pie -fno-stack-protector -o overflows-keep-flowing overflows-keep-flowing.c

void shutoff(long long int arg1) {
	printf("Phew. Another accident prevented. Shutting off %lld\n", arg1);
	if (arg1 == 0xdeadbeefd3adc0de) {
		execve("/bin/sh", NULL, NULL);
	} else {
		exit(0);
	}
}

int main() {
	char buf[0xff];
	gets(buf);
	puts(buf);
	return 0;
}
