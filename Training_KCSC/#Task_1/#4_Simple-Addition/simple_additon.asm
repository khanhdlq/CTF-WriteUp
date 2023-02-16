section .text
	global _start
_start:
	mov ecx,msg1		;msg1
	mov edx,len1
	call printf   
	
	mov ecx,str1		;in and output str1
	inc ecx
	mov edx,33
	call scanf
	
	mov ecx,msg2		;msg2
	mov edx,len2
	call printf
	
	mov ecx,str2		;in and output str2
	mov edx,33
	call scanf
	
	
	mov ecx,str1		;addition
	mov al,[ecx]
	add al,'0'
	mov [ecx],al
	mov edx,str2
	dec edx
	call addition
	call to0
	
	mov ecx,msg3		;print str3
	mov edx,len3
	call printf
	
	mov ecx,str1
	mov edx,33
	call printf
	
	call exit	
	
invert:
	mov al,[ecx]
	cmp al,0xa
	je done
	cmp al,'0'
	jb dec_ecx
	mov [edx],al
	jmp invert
	ret
	
dec_ecx:
	dec ecx
	mov al,'0'
	mov [ebx],al
	inc ebx
	jmp invert
	ret	

to0:				;value: 0123 -> 123
	mov ecx,str1
	mov al,[ecx]
	cmp al,'0'
	je to_0
	ret

to_0:
	mov al,0
	mov [ecx],al
	ret
	
addition: 
	inc ecx
	mov al,[ecx]
	cmp al,0xa
	je done
	sub al,'0'
	inc edx
	mov bl,[edx]
	sub bl,'0'	
	add al,bl
	cmp al,9
	ja above_9
	add al,'0'
	mov [ecx],al
	jmp addition
	ret
	
above_9:			;value:1a2 -> 202
	mov ebx,ecx
	jmp add
	ret	

add:
	sub al,10
	add al,'0'
	mov [ebx],al
	dec ebx
	mov al,[ebx]
	add al,1
	sub al,'0'
	cmp al,9
	ja add
	add al,'0'
	mov [ebx],al
	jmp addition
	ret


scanf: 
	mov eax,3
	mov ebx,0
	int 80h
	ret

printf:
	mov eax,4
	mov ebx,1
	int 80h
	ret

done:
	ret

exit:
	mov eax,1
	int 80h

section .bss 						;block starting symbol
	str1 resb 33
	str2 resb 33
	str3 resb 33

section .data
	msg1: db "Nhap so thu nhat: "
	len1 equ $ - msg1
	msg2: db "Nhap so thu hai: "
	len2 equ $ - msg2
	msg3: db "Tong cua 2 so la: "
	len3 equ $ - msg3
