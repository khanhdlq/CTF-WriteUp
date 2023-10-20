<?php
if(!empty($_SERVER['REQUEST_METHOD'])) //Thông tin về máy chủ và môi trường thực thi
{
    $path = 'C:\Users\C4t_f4t\Desktop\CODE\php\uploadfile\upload\\';
    move_uploaded_file($_FILES['uploaddi']['tmp_name'], $path.$_FILES['uploaddi']['name']);
    echo 'Đã upload file <span style="color: red;">'.$_FILES['uploaddi']['name'].'</span> vào <span style="color: blue;">'.$path.'</span>';
}
else 
    echo 'bbb';
?>      