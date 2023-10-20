<?php
    $i=0;
    $arr = array();
    $arr[$i++] = htmlentities($_GET["array"] ?? "", ENT_QUOTES, 'UTF-8');


    print_r($arr);
    echo '<br>';
    
    echo '<pre>';
    print_r($_POST);
    echo '</pre>';
?>