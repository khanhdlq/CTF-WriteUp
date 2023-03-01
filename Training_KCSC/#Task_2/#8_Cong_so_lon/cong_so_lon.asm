section .bss 						;Do bài này ở phần "SIMPLE_ADDITION" em đã sử dụng lưu vào mảng và cộng từng phần tử với nhau rồi nên em đã thay eax, ebx,... bằng rax, rbx,... 
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

	mov rcx,msg1					;msg1
	mov rdx,len1
	call printf   
	
	mov rcx,str1					;in and output str1
	inc rcx
	mov rdx,33
	call scanf
	mov [num1], rax
	mov [big_num], rax
	cmp rax,31
	ja too_big						;Bigger than 31bit then exit
	
	mov rcx,msg2					;msg2
	mov rdx,len2
	call printf
	
	mov rcx,str2					;in and output str2
	mov rdx,33
	call scanf
	mov [num2], rax
	
	cmp rax,31
	ja too_big						;Bigger than 31bit then exit
	
	mov rax, [num1]
	mov rbx, [num2]
	cmp rax, rbx		
	
	jb str1_big 					;Save the bigger value of len_str1 & len_str2  to big_num	
	call addition_ok 					;Start of calculation

done:
	mov rcx,msg3					;print msg3
	mov rdx,len3
	call printf
	
	mov rdi, sum					; 3+4 = 07 -> set 0 to null
	inc rdi
	mov al, [edi]
	cmp al, '0'
	jne hehe
	sub al,'0'
	mov [rdi], al
hehe:
	mov rcx,sum						;print sum
	add rcx,1
	mov rdx,33
	call printf
	
	call exit
;==============================================================================================================

;functions go here
						
str1_big:							;begin big_num = num2 and this make big_num = num1
	mov byte [big_num], 0	
	mov [big_num], rbx

addition_ok:						;consider 2 numbers in the same order 
	mov rax, str1			
	mov rbx, str2
	add rax, [num1]
	dec rax
	add rbx, [num2]
	sub rbx, 2	
addition:							;for ( ; big_num>0; big_num--)
	mov rdi, sum
	add rdi, [big_num]
	mov cl, [rax]
	cmp cl, 0
	je addcl						;if [num_1+n] = null -> add '0' for the sub '0' behind
con1:
	mov dl, [rbx]
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
	mov [rdi], cl
	dec rax
	dec rbx
	dec rdi
	sub byte [big_num], 1
	mov rbp, [big_num]
	mov [big_num], rbp
	cmp rbp, 0
	je done						;if [big_num] = 0 then end the program (loop [big_num] times)
	call addition

above9:	
	sub cl, 10
	mov byte [so_nho], 1
	call save

too_big:
	mov rcx, msg4
	mov rdx, len4
	call printf
	
	call exit

scanf: 
	mov rax,3
	mov rbx,0
	int 80h
	ret

printf:
	mov rax,4
	mov rbx,1
	int 80h
	ret

exit:
	mov rax,1
	int 80h

addcl: 
	add cl, '0'
	jmp con1




