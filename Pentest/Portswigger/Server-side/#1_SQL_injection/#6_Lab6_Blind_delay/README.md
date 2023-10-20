# Blind SQL injection with time delays

# 1. Vulnerable

Đây là 1 bài lab về `Blind SQLi`

`Blind SQLi` -> các câu lệnh có thực thi nhưng kết quả truy vấn SQL không trả về response

Vậy nên ta có 2 dạng `SQLi`

![blind.png](images/blind.png)

Yêu cầu của bài lab này là làm delay 10s tgian response

# 2.Exploit

Ở đây phần cookie sẽ chứa câu lệnh truy vấn phần `TrackingID` và có dạng

![id.png](image/id.png)

```
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'xPwmtukrdzxOEs1E'
```

Do ở đây kết quả truy vấn không được trả về cho người dùng nhưng các câu lệnh logic vẫn có thể thực hiện

Vậy mình đã thử và nhận được csdl ở đây được sử dụng đó là `PostgreSQL` và chuyển đổi nó thành câu truy vấn sau

```
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'xPwmtukrdzxOEs1E' || pg_sleep(10)--'
```

Ở phần này ta đã sử dụng toán tử nối chuỗi `||`

Nó sẽ thực hiện truy vấn phía sau để xác định chuổi đó thuộc kiểu dữ liệu nào để nối với chuỗi id phía trước. Từ đó khiến kết quả trả về bị delay 10s

payload sẽ là

```
'+||+pg_sleep(10)--
```

Và kết quả trang web bị delay và hoàn thành bài lab

![solved.png](image/solved.png)