# Lab: Reflected XSS into HTML context with nothing encoded

Đây là bài lab cơ bản về XSS 

![lab.png](images/lab.png)

Ở bài lab này ta chỉ cần làm trang web gọi đến câu lệnh `alert()` trong js là sẽ hoàn thành bài lab

# 1. Vulnerable

![lab1.png](images/lab1.png)

Trên url xuất hiện đoạn mã `/?search=abcd`

Khi ta gửi đoạn tìm kiếm `abcd` lên sever thì trên mã `HTML` của trang web sẽ thực hiện như sau

![lab2.png](images/lab2.png)

# 2. Exploit

Sẽ ra sao nếu ta sửa `abcd` thành 1 đoạn `javascript`

![lab3.png](images/lab3.png)

Như ta thấy ở đây thì đoạn js mà ta gửi lên sever đã hoạt động ngay trong mã HTML và ta đã giải quyết được bài lab ez này