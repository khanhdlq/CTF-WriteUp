section .bss 						
	str1 resb 33					;value1 
	num1 resb 33					;len_value1
	str2 resb 33					;value2
	num2 resb 33					;len_value2
	sum resb 33						;sum of 2 value
	so_nho resb 2					;9+8 = 17 -> 1 is [so_nho]
	big_num resb 33					;the bigger of len_value1 & len_value2 is big_num (len_of_value3)

section .data
	msg1: db "Nhap so thu nhat: "
	len1 equ $ - msg1
	msg2: db "Nhap so thu hai: "
	len2 equ $ - msg2
	msg3: db "Tong cua 2 so la: "
	len3 equ $ - msg3
	msg4: db "Toi da 31 bit"
	len4 equ $ - msg4

;==============================================================================================================

section .text
	global _start
_start:
	mov word [str1], 0				;setup all value to null bytes
	mov word [str2], 0
	mov word [sum], 0
	mov word [str1-8], 0
	mov word [str2-8], 0
	mov word [sum-8], 0
	mov word [str1-16], 0
	mov word [str2-16], 0
	mov word [sum-16], 0
	mov word [str1-24], 0
	mov word [str2-24], 0
	mov word [sum-24], 0

	mov ecx,msg1					;msg1
	mov edx,len1
	call printf   
	
	mov ecx,str1					;in and output str1
	inc ecx
	mov edx,33
	call scanf
	mov [num1], eax
	mov [big_num], eax
	cmp eax,31
	ja too_big						;Bigger than 31bit then exit
	
	mov ecx,msg2					;msg2
	mov edx,len2
	call printf
	
	mov ecx,str2					;in and output str2
	mov edx,33
	call scanf
	mov [num2], eax
	
	cmp eax,31
	ja too_big						;Bigger than 31bit then exit
	
	mov eax, [num1]
	mov ebx, [num2]
	cmp eax, ebx		
	
	jb str1_big 					;Save the bigger value of len_str1 & len_str2  to big_num	
	call addition_ok 					;Start of calculation

done:
	mov ecx,msg3					;print msg3
	mov edx,len3
	call printf
	
	mov edi, sum					; 3+4 = 07 -> set 0 to null
	inc edi
	mov al, [edi]
	cmp al, '0'
	jne hehe
	sub al,'0'
	mov [edi], al
hehe:
	mov ecx,sum						;print sum
	add ecx,1
	mov edx,33
	call printf
	
	call exit
;==============================================================================================================

;functions go here
						
str1_big:							;begin big_num = num2 and this make big_num = num1
	mov byte [big_num], 0	
	mov [big_num], ebx

addition_ok:						;consider 2 numbers in the same order 
	mov eax, str1			
	mov ebx, str2
	add eax, [num1]
	dec eax
	add ebx, [num2]
	sub ebx, 2	
addition:							;for ( ; big_num>0; big_num--)
	mov edi, sum
	add edi, [big_num]
	mov cl, [eax]
	cmp cl, 0
	je addcl						;if [num_1+n] = null -> add '0' for the sub '0' behind
con1:
	mov dl, [ebx]
	cmp dl, 0
	jne con
	add dl, '0'						;if [num_2+n] = null -> add '0' for the sub '0' behind
con:			
	sub cl, '0'
	cmp cl, 20						;số linh tinh cho về 0 hết :))
	jb above20
	mov cl, 0
above20:
	sub dl, '0'
	add cl, dl						;sum 2 value and add to cl
	add cl, [so_nho]					;add [so_nho] to cl
	
	mov byte [so_nho], 0
	cmp cl, 9
	ja above9						;if a = 11 > 9 -> a sub 10 = 1 and [so_nho] = 1
		
save:								;save cl to edi = sum and dec the addr of value1; value2; sum
	add cl, '0'
	mov [edi], cl
	dec eax
	dec ebx
	dec edi
	sub byte [big_num], 1
	mov ebp, [big_num]
	mov [big_num], ebp
	cmp ebp, 0
	je done						;if [big_num] = 0 then end the program (loop [big_num] times)
	call addition

above9:	
	sub cl, 10
	mov byte [so_nho], 1
	call save

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
	jmp con1




