# png-in-a-jpg-stack 

- Ở bài này sẽ cho chúng ta 1 file gồm nhiều ảnh

![png.png](images/png.png)

- Ngay phần đầu bài chúng ta nhận được 1 hint đó là có 1 file đặc biệt

![hint1.png](images/hint1.png)

- Mình đã sort by type và đã phát hiện file đặc biệt đó ở cuối

![spec.png](images/spec.png)

- Kế đến có hint thứ 2 đó là mỗi file đều có 1 comment

![hint2.png](images/hint2.png)

- Mình check stings file bằng command `file`

![cmt.png](images/cmt.png)

- Sử dụng base64 decode và nhận được flag 

![base64.png](images/base64.png)

# Flag: jctf{shell_scripting_is_awesome}