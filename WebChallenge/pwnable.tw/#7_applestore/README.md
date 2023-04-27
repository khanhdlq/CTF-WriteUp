# pwnable.tw - Applestore

# 1. Xem thông tin file

Ta sẽ dùng lệnh `file` để xem thông tin file challenge:
```
applestore_patched: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter ./ld-2.23.so, for GNU/Linux 2.6.24, BuildID[sha1]=35f3890fc458c22154fbc1d65e9108a6c8738111, not stripped

```
Đây là file 32-bit không bị ẩn tên hàm. Kế đến, ta sẽ kiểm tra security của file:
```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8047000)
RUNPATH:  b'.'
```

Tiếp đến đưa file vào ida-32bit, ở đây mình đã sửa lại tên một số hàm và biến để dễ quan sát luồng thực thi

![gdb.png](images/gdb.png)

# 2. Ý tưởng

Bài này là 1 danh sách liên kết 2 chiều. Mỗi khi ta add thêm 1 sản phẩm vào thì nó sẽ thêm node ấy vào cuối danh sách bằng hàm `insert()`

![insert.png](images/insert.png)

Dòng thứ hai khai báo con trỏ "i" kiểu "_DWORD" và gán giá trị là địa chỉ của biến "myCart".

Trong vòng lặp "for", hàm duyệt qua các phần tử trong danh sách liên kết, bắt đầu từ địa chỉ của biến "myCart". Vòng lặp sẽ tiếp tục cho đến khi i[2] bằng 0,

tức là đến khi phần tử cuối cùng trong danh sách được tìm thấy.

Sau khi tìm thấy phần tử cuối cùng trong danh sách, con trỏ "i" trỏ đến phần tử cuối cùng đó. Dòng tiếp theo của hàm thêm phần tử mới vào cuối danh sách 

bằng cách gán giá trị của biến "a1" cho i[2].

Dòng tiếp theo của hàm cập nhật con trỏ phần tử trước đó của phần tử mới được thêm vào danh sách. Điều này đảm bảo rằng danh sách liên kết được duy trì.

Tiếp đến ta có hàm `check()`

![check.png](images/check.png)

Đầu tiên ta có thể thấy điều đặc biệt ở hàm check đó là nếu tổng giá trị của sản phẩm = 7174$

thì sẽ cho ta phần thưởng là 1 iPhone 8 - 1$

* Mình không kiếm được hàm `free()` ở đây nên không `heap_exploit` được

![compare.png](images/compare.png)

Mình thấy sự khác biệt giữa 2 hàm được thêm bằng `insert()` này:

Riêng `iPhone 8 - 1$` được lưu trên stack còn lại được lưu trên heap

# 3. Khai thác

- Bước 1: Nhận iphone-8 

```
for i in range(6):
		add(1)
for i in range(20):
		add(2)
checkout()
```

- Bước 2: Leak libc, stack

![checkout.png](images/checkout.png)

Nhìn vào đây và nhìn vào hàm delete 

![checkout2.png](images/checkout2.png)

Do ở đây sẽ sử dụng con trỏ để in ra giá trị tại địa chỉ mà nó trỏ tới mỗi khi ta delete 1 item ấy(cụ thể là tên đã được gán khi cấp phát)

Nhận ra khi người ta trao ip8 cho ta, con trỏ `v2` đã được cấp phát tại vị trí `ebp-0x20` mà tại `delete()` ta có quyền viết `0x15` ký tự tại địa chỉ `ebp-0x22`

-> Toàn quyền thay đổi con trỏ ấy và mình đã dùng để leak địa chỉ libc cũng như địa chỉ stack

- Bước 3: Get_shell

OKe vậy đã có các giá trị, địa chỉ, ta sẽ xem thử các thanh ghi ở địa chỉ `ebp-0x20` làm gì

```
delete(b"27" + cyclic(0x30))
```

![gdb2.png](images/gdb2.png)

Vậy là giá trị tại địa chỉ `ebp-0x14` sẽ lưu vào `[ebp-0x10]` + 8

Và sau đó giá trị tại địa chỉ `ebp-0x10` sẽ lưu vào `[ebp-0x14]` + 12

![gdb3.png](images/gdb3.png)

Với điều kiện ấy, đầu tiên mình sẽ đưa `atoi@got.plt+0x22` vào `ebp` 

Tại sao lại là `atoi@got.plt+0x22`?

![eax.png](images/eax.png)

Nhìn vào stack sau khi đưa vào ta có `lea eax, [ebp - 0x22]` và vì vậy `eax = atoi@got.plt`

![myread.png](images/myread.png)

Vậy là khi vào hàm `readme()`:

`result` = `eax` = `atoi@got.plt`

Những gì ta nhập tiếp sẽ lưu vào `atoi@got.plt`

=> Mình sẽ ghi `system` vào đây 

```
p.sendline(p32(libc_system))
```

Sau khi đã ghi `system` vào `atoi@got.plt` thì những gì mình đã nhập vào sẽ theo đó thực thi

=> thêm chuỗi `;/bin/sh;`: dấu `;` để ngăn cách `/bin/sh` với các command liền kề nó 

```
p.sendline(p32(libc_system) + b";/bin/sh;")
```

![flag.png](images/flag.png)

