section .text 
	global _start
	
_start: 
	mov eax,4
	mov ebx,1
	mov ecx,msg
	mov edx,len
	int 80h
		
	mov eax, 1
	int 80h

section .data
	msg: db 'Hello,World!', 0xa
	len equ $ - msg
