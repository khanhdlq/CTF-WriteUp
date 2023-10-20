<?php
$admin = 'admin';
$pass = 'adminne';
$email = 'quockhanh03.bg@gmail.com';
$value1 = htmlentities($_GET["username"] ?? 0, ENT_QUOTES, 'UTF-8');
$value2 = htmlentities($_GET["password"] ?? 0, ENT_QUOTES, 'UTF-8');
$value3 = htmlentities($_GET["email"] ?? 0, ENT_QUOTES, 'UTF-8');
$p = htmlentities($_GET["p"] ?? 0, ENT_QUOTES, 'UTF-8');

if ($value1===$admin && $value2===$pass && $value3===$email)
{
    require 'admin.php';
    exit();
}
$path = 'C:\\Users\\C4t_f4t\\Desktop\\CODE\\php'.$p;
echo file_get_contents($path);
echo 'Login falled';
?>