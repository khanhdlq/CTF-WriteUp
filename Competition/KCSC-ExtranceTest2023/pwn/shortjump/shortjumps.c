#include <stdio.h>
#include <stdlib.h>

int jmp = 0;

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

int jmp1(int a)
{
	if (a==0xdeadbeef)
		jmp++;
}

int jmp2(int a, int b)
{
	char command[8] = {0};
	command[0] = '/';
	command[1] = 'b';
	command[2] = 'i';
	command[3] = 'n';
	command[4] = '/';
	command[5] = 's';
	command[6] = 'h';
	command[7] = '\0';

	if (jmp!=1)
	{
		puts("Don't cheat, hacker!");
		exit(0);
	}
	if (a==0xcafebabe && a+b==0x13371337)
		system(command);
}

int main()
{
	char name[0x20];
	char dream[0x50];
	char choose = 'Y';

	init();
	puts("Hi, what's your name?");
	printf("> ");
	scanf("%31s", name);
	getchar();

	puts("Do you have any dream? [Y/n]");
	printf("> ");
	scanf("%c", &choose);

	if (choose=='Y' || choose=='y' || choose=='\n')
	{
		puts("Tell me your dream!");
		printf("> ");
		scanf("%140s", dream);
		getchar();
		puts("Wow, that's interesting!");
	}
}