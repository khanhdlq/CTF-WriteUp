<?php
session_start();
echo "<h2>Do you need phpinfo? ... or not?</h2>";

$num=$_GET['num'];
$page=$_GET['page'];

if(preg_match("/^[0-9+-\/\*e ]/i", $num)){
    exit("<h2>I hate number<h2>");
}

if(preg_match("/flag|\.|php|conf|\*|'|\"/i", $page)){
    exit("<h2>don't do that.</h2>");
}


if(!is_numeric($num)){
    echo('Bypassed numeric');
    if($page==null){
        echo phpinfo();
    }else{
        include_once($page);
    }
}else{
    highlight_file(__FILE__);
}

?>