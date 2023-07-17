# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

# 1. Vulnerable

Hint:
- This lab contains a `SQL injection` vulnerability in the `product category filter`. When the user selects a category, the application carries out a `SQL query` like the following:
```
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```
- To solve the lab, perform a `SQL injection` attack that causes the application to display one or more unreleased products.

Ở đây ta nhận được `SQL query form` với cách lấy 1 trường trong `category` là `Gifts` và `released` = 1

Nhìn trên url thì đúng là nó sẽ lấy tên của 1 danh mục sản phẩm rồi hiện thông tin lên cho ta xem

[web.png](images/web.png)

# 2. Exploit

Vậy nếu ta sử dụng câu lệnh or thì sao nhỉ

Ta thêm vào `' or 1=1--` thì câu lệnh SQL sẽ như sau:

```
SELECT * FROM products WHERE category = 'Gifts' or 1=1--' AND released = 1
```

Sau khi thêm vào thì ta sẽ có câu lệnh logic đó là: lấy tất cả giá trị từ `products` nếu `category = 'Gifts'` hoặc `1=1`. Còn dấu `--` phía sau sẽ loại bỏ đi các câu lệnh phía sau nó

Do ở đây 1=1 luôn đúng nên ta sẽ nhận được mọi giá trị từ trường `products`

Ok vậy ta sẽ sửa ở phần GET trong `burpsuite` 

```
GET /filter?category=Gifts'+or+1=1-- HTTP/2
```

Và trang web đã hiện lên tất cả những sản phẩm có trong `products`

[solved.png](images/solved.png)

