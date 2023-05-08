# Bdides_algiers_2023 - Broken_Base64

Đề bài cho 1 đoạn mã base64-encode 

```
lbGxtYXRlc3tZMHVfaDRWM183MF91TmQzcjV0NG5EX0gwd19CNDUzNjRfdzBSazV9 flag format: shellmates{…}
```

Mình thấy họ cho `flag format: shellmates{…}` như 1 gợi ý và mình đã dùng base64_encode đoạn `shellmates{` và được `c2hlbGxtYXRlc3s=`

Giống với đoạn base64 bài cho nhưng đầu bài đã thiếu 3 bytes đầu. Mình thêm 3 bytes đầu của đoạn `shellmates{` vào và dùng base64_decode và nhận được flag

# Flag: shellmates{Y0u_h4V3_70_uNd3r5t4nD_H0w_B45364_w0Rk5}