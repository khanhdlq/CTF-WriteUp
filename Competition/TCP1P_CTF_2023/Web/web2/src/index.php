<?php
require("vendor/autoload.php");

if (isset($_COOKIE['cookie'])) {
    $cookie = base64_decode($_COOKIE['cookie']);
    $cook = `O:4:"Vuln":1:{s:3:"cmd";s:17:"system('whoami');";}`;
    $var1 = unserialize($cook);
    print_r($var1);
}
