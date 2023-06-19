#include <stdio.h>
#include <stdlib.h>

// gcc -no-pie -fno-stack-protector -o overflow-in-the-fl4gtory overflow-in-the-fl4gtory.c

void shutoff() {
	printf("Pipe shut off!\n");
	printf("Congrats! You've solved (or exploited) the overflow! Get your flag:\n");
	execve("/bin/sh", NULL, NULL);
}


int main() {
	char buf[0xff];
	gets(buf);
	puts(buf);
	return 0;
}
