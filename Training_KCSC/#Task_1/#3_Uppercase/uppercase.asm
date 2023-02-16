section .text
	global _start
	
_start:
	mov ecx, string
	call scanf
	mov ecx,string
	call Upper
	
	mov ecx,string
	call printf
	
	call exit
	
Upper:
	mov al,[ecx]
	cmp al,0x0
	je done
	cmp al,'a'
	jb next_char
	cmp al,'z'
	ja next_char
	sub al,0x20
	mov [ecx],al
	jmp next_char
	int 80h
	
next_char:
	inc ecx
	jmp Upper
	int 80h
	
scanf: 
	mov eax,3
	mov ebx,1
	mov edx,32
	int 80h
	ret
	
printf:
	mov eax,4 
	mov ebx,1 
	mov edx,32
	int 80h
	ret

exit:
	mov eax,1
	int 80h
	ret
	
done:	
	ret
	
section .bss
	string resb 32

	
