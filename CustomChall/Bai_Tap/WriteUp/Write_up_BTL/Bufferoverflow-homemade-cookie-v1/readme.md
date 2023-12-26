# BÀI TẬP LỚN KHAI THÁC LỖ HỔNG PHẦN MỀM

- Bài 2: Bufferoverflow-homemade-cookie-v1

Ở đây mình đã được cung cấp source code của bài này

![src.png](images/src.png)

Ở đây ta cần chú ý đến 2 hàm đó là hàm `vun()`

```
void vun()
{
int i = 0xc00c1e;
char buff[16];
gets(&buff);
printf("%s", buff);
    if (i != 0xc00c1e)
    {
        printf("DONT SMASH THE STACK PLZ!\n");
        exit(0);
    }
}
```

và hàm `cat_flag()` để ta lấy flag

```
int cat_flag()
{
system("cat flag");
}
```

Đầu tiên ta sẽ phân tích luồng thực thi của chương trình bằng `gdb`, nhưng trước đó ta cần cấp full quyền cho file `Bufferoverflow-homemade-cookie-v1` bằng câu lệnh 

```
chmod 777 ./Bufferoverflow-1-byte
```

Ở bài này hãy cũng nhau đọc source code:

Ta thầy ở hàm `vun()` biến buff được cấp phát 16 bytes nhưng chương trình lại sử dụng hàm `gets()`, đây là lỗi rất nhiều lập trình viên mắc phải đó là: không kiểm soát số lượng ký tự đầu vào của chương trình dẫn đến lỗi buffer overflow

Tiếp đến, chương trình sẽ so sánh biến `i` được cấp phát ban đầu xem nó có bị thay đổi gì hay không, nếu biến `i` bị thay đổi, chương trình sẽ in ra dòng chữ `DONT SMASH THE STACK PLZ!`

Chúng ta sẽ sử dụng gdb để xem luồng thực thi chương trình

![gdb0.png](images/gdb0.png)

Nhìn vào đoạn mã assembly, ta có thể thấy biến `i` nằm ở vị trí [ebp-0xc] với giá trị tại địa chỉ ấy là `0xc00c1e`, địa chỉ lưu chuỗi input của ta là [ebp-0x1c] chính là giá trị của thanh ghi `eax`

Ta luôn biết được địa chỉ trả về (return_address) của hàm `vun()` luôn nằm tại vị trí [ebp+0x4] mà biến buff của ta được lưu tại địa chỉ [ebp-0x1c], cộng với hàm `gets()` cho ta thoải mái nhập số lượng ký tự

-> Ta chỉ cần overwrite 0x20 bytes và 4 bytes còn lại là địa chỉ của hàm `cat_flag()` thì ta sẽ ghi đè địa chỉ trả về khiến sau khi kết thúc hàn `vun()`, chương trình sẽ gọi hàm `cat_flag()` và ta sẽ lấy được flag

Ở đây có điều kiện là không được thay đổi giá trị của `i` - chính là giá trị tại địa chỉ [ebp-0xc]

=> payload của ta sẽ bao gồm: 
+ 16 bytes để đến địa chỉ `i`
+ 4 bytes giá trị tại địa chỉ `i` ban đầu
+ 12 bytes tiếp theo đến đến return_addr
+ 4 bytes cuối ghi đè ret_addr thành địa chỉ hàm `cat_flag()`

```
python2 -c 'print "a"*0x10 + "\x1e\x0c\xc0\x00" + "a"*0xc + "\xcb\x84\x04\x08"'
```

![flag.png](images/flag.png)