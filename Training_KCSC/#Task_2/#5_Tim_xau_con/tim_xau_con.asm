section .bss 						 
	str1 resb 100					
	num1 resb 10					
	str2 resb 100
	num2 resb 10
	dem resb 100
	value resb 10
	value_to_print resb 20
	address resb 200
	print_value resb 200	
	print_value2 resb 200
section .data
	msg1: db "Nhap day thu nhat: "
	len1 equ $ - msg1
	msg2: db "Nhap day thu hai: "
	len2 equ $ - msg2
	new_line: db 0xa
	len3 equ $ - new_line
	new_space: db 0x20
	len4 equ $ - new_space

;==============================================================================================================

section .text
	global _start


addi:	
	mov rax, [rcx]
   	mov rbx, 10             	;chia số nguyên cho 10 để lấy từng chữ số
	mov r8, 0 
num_to_str_loop:
	xor rdx, rdx
    	div rbx                  	;chia rax cho 10
    	add rdx, '0'            	;cộng thêm mã ASCII của '0' để đổi sang ký tự 
	mov [print_value+r8], rdx      ;đẩy ký tự vào biến print_fibo
    	inc r8                 		;tăng đếm số chữ số đã đổi sang ký tự
    	cmp rax, 0 
    	jne num_to_str_loop     	;lặp lại nếu chưa đổi xong
	mov rax, [print_value]		
	mov [print_value2], rax
	mov rbx, [print_value]
	cmp rbx,0x40			;với trường hợp chỉ có 1 chữ số thì lưu luôn vào print_fibo2 rồi bỏ qua loop_start
	jb priint
	
	
loop_start_here:					;hàm này dùng để đảo ngược chuỗi print_fibo và lưu vào print_fibo2
      mov rax, print_value
	mov rdx, print_value2
	add rax, 199			;loop từ print_fibo+199 đến khi k còn ký tự 0x00

loop_x:		
	dec rax
	mov bl, [rax]
	cmp bl, 0
	jz loop_x
	mov [rdx], bl
	inc rdx
	cmp rax, print_value
	jz done
	call loop_x					
	
priint:
	mov rcx, print_value2		;in ra số hex đầu vào dưới dạng ASCII dec
	mov rdx, 190
	call printf	

	mov rcx, new_space      	
    	mov rdx, len4			
    	call printf				;in ký tự ngăn cách giữa các số ' '
	jmp done
	
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

done: 
	ret

print_addr:
	mov r10, address				;địa chỉ chuỗi ví dụ: 0x0c05 vào r10
print_addr2:
	mov cl, [r10]				;tách từng byte để chuyển về ASCII DEC
	inc r10
	cmp cl, 0					;nếu đến ký tự 0 nghĩa là đã hết cái cần so sánh
	je done
	sub cl ,1
	mov [value_to_print], cl		;chuyển byte vào biến value_to_print
	mov rcx, value_to_print			;chuyển biến value_to_print vào thanh ghi rcx để chuyển sang ASCII DEC
	call addi
	jmp print_addr2

_start:	
	mov rcx, str1
	mov rdx, 100
	call scanf					;nhập đoạn chuỗi 'S = abcd'

	mov rcx, str2
	mov rdx, 100
	call scanf					;nhập đoạn chuỗi 'C = abcd'
	sub rax, 0x5				;trừ đi đoạn 'C = ' để lưu độ dài chuyển vào num2
	mov [num2], rax

	call find_string				;bắt đầu hàm tính toán
	
	mov rcx, value
	call addi
	
	mov rcx, new_line
	mov rdx, len3
	call printf

	call print_addr

	mov rcx, new_line
	mov rdx, len3
	call printf
	
	call exit
	

;==============================================================================================================


find_string:
	mov rax, str1
	mov rbx, str2
	add rax, 0x4			;loại bỏ ký tự 'S = ' khỏi xâu S
	add rbx, 0x4			;loại bỏ ký tự 'C = ' khỏi xâu C
loop_start:
	xor rcx, rcx
	xor rdx, rdx
	inc dword [dem]			
	mov cl, [rax]
	mov dl, [rbx]
	cmp cl, 0xa				;loop đến khi gặp ký tự xuống dòng của chuỗi chính thì end 
	je done
	cmp cl, dl
	jnz inc_rax				;nếu 2 ký tự khác nhau thì nhảy qua ký tự tiếp theo
	
	jmp loop_2				;nếu 2 ký tự đầu bằng nhau thì so sánh phần còn lại của chuỗi C

inc_rax:
	inc rax	
	jmp loop_start

loop_2:				
	mov r8, rax				;phần còn lại của chuỗi chính đang cần so sánh
	mov r9, rbx				;chuỗi con
	mov r10, [num2]			;số ký tự chuỗi con để loop

loop_3:
	inc r8				;tăng địa chỉ r8 để so sánh ký tự tiếp theo của chuỗi chính và chuỗi con
	inc r9
	mov cl, [r8]			
	mov dl, [r9]
	cmp dl, 0xa				;nếu chuỗi con kết thúc bằng '\n' thì tăng 'value' (là số lần xuất hiện chuỗi con) và tăng địa chỉ chuỗi chính lên 1 để tiếp tục so sánh phần sau
	je loop_4
	cmp cl, dl
	jnz loop_5				;2 ký tự khác nhau thì lại tăng địa chỉ chuỗi chính lên 1 để tiếp tục so sánh phần sau
	cmp cl,0xa
	je loop_start			;nếu gặp ký tự xuống dòng của chuỗi chính thì end
	jmp loop_3				;nếu k gặp các điều kiện trên thì lại tiếp tục so sáng các ký tự giống nhau tiếp theo của 2 chuỗi

loop_4:
	inc dword [value]
	
	mov r8, address		 	;biến address để lưu vị trí xuất hiện của xâu con theo từng byte ví dụ ở vị trí 5 và 12 -> [address] = 0x0c05
	dec r8
loopp:
	inc r8
	mov dl, [dem]			
	mov cl, [r8]
	cmp cl, 0
 	jnz loopp				;nếu ở địa chỉ byte hiện tại của r8(là địa chỉ của address sau khi inc r8 nhiều lần) đã chứa giá trị thì lại tăng r8 lên để lưu tiếp các giá trị
	mov [r8], dl

	inc rax
	jmp loop_start
	
loop_5:
	inc rax
	jmp loop_start

;S = Cong hoa xa hoi chu nghia Viet Nam
;C = ho
	
	


