section .bss                      
	num resb 100						;N value
	hexval resb 20						;N to int value to loop
	demdem resb 20
    	value1 resb 32						;caculation fibonaci
    	value2 resb 32						
    	value resb 32						;fibonaci number
	multi resb 2						;ex: 1234 -> use to mul 4 with 1, 3 with 10, 2 with 100...
	print_fibo resb 200	
	print_fibo2 resb 200		
	big_num resb 33						;the bigger of len_value1 & len_value2 is big_num (len_of_value3)
section .data
    	msg1: db "Nhap so N: "
    	len1 equ $ - msg1
    	msg2: db "Day so fibonaci gom "
    	len2 equ $ - msg2
	msg3: db " so hang dau tien la: "
    	len3 equ $ - msg3
	next_line: db 0xa
	len4 equ $ - next_line
	space : db " "
	len5 equ $ - space
;============================================================================================================

section .text
    global _start
;Các hàm ở đây
printf_text:							;printf 'Day so fibonaci gom % so hang dau tien la: '
	dec rax
    	mov rcx, num
	add rcx, rax 							
	mov byte [rcx], 0x0
	xor rcx,rcx
	
	mov rcx,msg2      					;Day so fibonaci gom 
    	mov rdx,len2
    	call printf

	mov rcx, num						;%s
	mov rdx, 100
	call printf

	mov rcx, msg3						;so hang dau tien la: 
	mov rdx, len3
	call printf

string2hex:		
	mov rax, num
	add rax, rdi						;go to last char of num
	mov rdx, [demdem]
	sub rax, rdx						
	mov rbx, rax
	xor rax, rax
	mov al, [rbx]						;mov al, 	order number
	xor rbx, rbx
	cmp al, 0
	je done							;if char = null -> break
	
	sub al, '0'
	mov rbx, [multi] 
	mul rbx	
	add [hexval], rax					;hexval += number * 10^2
	
	mov rcx, 10							
	mov rax, [multi]
	mul rcx							
	mov [multi],rax						;multi pow 10
	xor rax, rax
	inc byte [demdem]
	jmp string2hex
	 
;============================================================================================================
loop_fibonaci:
	mov rax, [hexval]			;so sánh xem còn số lần loop không
	cmp rax, 0
	je done	
	dec byte [hexval]			;vẫn loop đc thì giảm hexval xuống
	mov rbx, [value1]			;giá trị 1 vào rbx
	mov rcx, [value2]			;giá trị 2 vào rcx
	add rbx, rcx
	mov [value], rbx			;cộng vào rồi đưa vào value in ra
	mov [value1], rcx			;value1 = value2
	mov [value2], rbx			;value2 = value vừa in ra
	xor rax, rax
	xor rbx, rbx
	xor rcx, rcx
	xor rdx, rdx
	mov rcx, value			;đưa value dưới dạng hex để in ra dưới dạng ASCII dec
	call addi
	jmp loop_fibonaci

addi:	
	mov rax, [rcx]
   	mov rbx, 10             	;chia số nguyên cho 10 để lấy từng chữ số
	mov r8, 0 
num_to_str_loop:
	xor rdx, rdx
    	div rbx                  	;chia rax cho 10
    	add rdx, '0'            	;cộng thêm mã ASCII của '0' để đổi sang ký tự 
	mov [print_fibo+r8], rdx      ;đẩy ký tự vào biến print_fibo
    	inc r8                 		;tăng đếm số chữ số đã đổi sang ký tự
    	cmp rax, 0 
    	jne num_to_str_loop     	;lặp lại nếu chưa đổi xong
	mov rax, [print_fibo]		
	mov [print_fibo2], rax
	mov rbx, [print_fibo]
	cmp rbx,0x40			;với trường hợp chỉ có 1 chữ số thì lưu luôn vào print_fibo2 rồi bỏ qua loop_start
	jb priint
	
	
loop_start:					;hàm này dùng để đảo ngược chuỗi print_fibo và lưu vào print_fibo2
      mov rax, print_fibo
	mov rdx, print_fibo2
	add rax, 199			;loop từ print_fibo+199 đến khi k còn ký tự 0x00
loop_x:		
	dec rax
	mov bl, [rax]
	cmp bl, 0
	jz loop_x
	mov [rdx], bl
	inc rdx
	cmp rax, print_fibo
	jz done
	call loop_x					
	
priint:
	mov rcx, print_fibo2		;in ra số hex đầu vào dưới dạng ASCII dec
	mov rdx, 190
	call printf	

	mov rcx, space      	
    	mov rdx, len5			
    	call printf				;in ký tự ngăn cách giữa các số ' '
	call loop_fibonaci

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
done:
	ret

exit:
    	mov rax,1
    	int 80h
;============================================================================================================

_start:
	mov qword [value1], 1 					;1st value in fibonaci
	mov qword [value2], 1 					;2nd value in fibonaci
	mov qword [value], 0x31
	mov qword [multi], 1 					;ex: 1234 -> use to mul 4 with 1
	mov qword [print_fibo2], 0
	mov qword [num], 0
    	mov rcx,msg1        					;msg1
    	mov rdx,len1
    	call printf   
    
    	mov rcx, num
	mov rdx, 100
	call scanf
	mov rdi, rax
	sub rdi, 2						;go to the first char of string input 				
	call printf_text
	
	call string2hex					;chuyển từ chuỗi string sang hex

	cmp qword [hexval], 0				;đầu vào là 0 thì chương trình exit
	jz exit

	mov rcx, value
	mov rdx, 2
	call printf						;in số đầu tiên là 1

	mov rcx, space
	mov rdx, len5
	call printf
	
	cmp qword [hexval], 1				;đầu vào là 1 thì chương trình in ra 1 số 1
	jz exit

	mov rcx, value
	mov rdx, 2
	call printf						;in số thứ 2 là 1
	sub qword [hexval],2				;giảm hexval đi 2 do in ra 2 số 1

	mov rcx, space
	mov rdx, len5
	call printf
	
	call loop_fibonaci
	mov rcx, next_line
	mov rdx, len4
	call printf

    	call exit	

;============================================================================================================


