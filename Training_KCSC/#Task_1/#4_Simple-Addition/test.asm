section .bss 						;block starting symbol
	str1 resb 33
	num1 resb 10
	str2 resb 33
	num2 resb 10
	sum resb 33
	so_nho resb 2
	big_num resb 10

section .data
	msg1: db "Nhap so thu nhat: "
	len1 equ $ - msg1
	msg2: db "Nhap so thu hai: "
	len2 equ $ - msg2
	msg3: db "Tong cua 2 so la: "
	len3 equ $ - msg3
	msg4: db "Toi da 31 bit"
	len4 equ $ - msg4

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
	mov [num1], eax
	cmp eax,31
	ja too_big			;Bigger than 31bit then exit
	
	mov ecx,msg2		;msg2
	mov edx,len2
	call printf
	
	mov ecx,str2		;in and output str2
	mov edx,33
	call scanf
	mov [num2], eax
	mov [big_num], eax
	dec byte [big_num]
	cmp eax,31
	ja too_big			;Bigger than 31bit then exit
	
	mov eax, [num1]
	mov ebx, [num2]
	cmp eax, ebx
	ja str1_big 		;Save the bigger value of len_str1 & len_str2  to big_num	
		
done:
	mov ecx,msg3		;print msg3
	mov edx,len3
	call printf
	
	mov ecx,sum			;print sum
	add ecx,1
	mov edx,33
	call printf
	
	call exit
;============================================================================
addition_ok:
	mov eax, str1
	mov ebx, str2
	add eax, [num1]
	dec eax
	add ebx, [num2]
	sub ebx, 2
	call addition
	
addition:
	mov edi, sum
	add edi, [big_num]
	mov cl, [eax]
	cmp cl, 0
	je addcl
	mov dl, [ebx]
	cmp dl, 0
	jne con
	add dl, '0'

con:	
	sub cl, '0'
	sub dl, '0'
	add cl, dl			;cong 2 so luu vao cl
	add cl, [so_nho]		;cong them phan nho 1 hoac 0 vao cl
	
	mov byte [so_nho], 0
	cmp cl, 9
	ja above9
	
save:
	add cl, '0'
	mov [edi], cl
	dec eax
	dec ebx
	dec edi
	sub byte [big_num], 1
	mov ebp, [big_num]
	mov [big_num], ebp
	cmp ebp, 1
	jz done
	call addition

above9:	
	sub cl, 0xa
	mov byte [so_nho], 1
	call save

str1_big:
	mov byte [big_num], 0
	mov [big_num], eax
	call addition_ok

too_big:
	mov ecx, msg4
	mov edx, len4
	call printf
	
	call exit


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

exit:
	mov eax,1
	int 80h

addcl: 
	add cl, '0'
	jmp con



