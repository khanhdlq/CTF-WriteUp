section .text
	global _start

_start:	
	mov eax,3
	mov ebx,0
	mov ecx,string
	mov edx,32
	int 80h
	
	mov eax,4
	mov ebx,1
	mov ecx,string
	mov edx,32
	int 80h
	
	mov eax,1
	int 80h


section .bss
	string resb 32
	
