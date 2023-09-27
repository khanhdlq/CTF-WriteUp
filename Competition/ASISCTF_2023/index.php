<?php
/*
Read /next.txt
Hint for beginners: read curl's manpage.
*/

highlight_file(__FILE__);

$url = 'file:///hi.txt';

if (
    array_key_exists('x', $_GET) &&
    !str_contains(strtolower($_GET['x']), 'file') &&
    !str_contains(strtolower($_GET['x']), 'next')
) {
    $url = $_GET['x'];
}

system('curl ' . $url);
echo $url;

?>
