<?php

    require_once("config.php");
    session_start();



    $query = isset($_GET['query']) ? $_GET['query'] : "";

    if(!empty($query)){
        $url = httpProxy($query);
        sendProxy($url);
    }else{
        header("Location: leaderboard.php");
    }


    function sendProxy($url){
        $curl = curl_init();
        if ($_SERVER["REQUEST_METHOD"] === "GET") {
            $options = array(
                CURLOPT_URL => $url,
                CURLOPT_HTTPGET => true,
                CURLOPT_RETURNTRANSFER => true,
            );
            curl_setopt_array($curl, $options);
        }
        if ($_SERVER["REQUEST_METHOD"] === "POST") {
            curl_setopt($curl, CURLOPT_POST, true);
            $data = $_POST;
            $options = array(
                CURLOPT_URL => $url,
                CURLOPT_POST => true,
                CURLOPT_POSTFIELDS => http_build_query($data),
                CURLOPT_RETURNTRANSFER => true,
            );
            curl_setopt_array($curl, $options);
        }
        
        $headers = array(
            'X-Access-Token: '.base64_encode($_SESSION['username'].':'.$_SESSION['password']),
        );
        if($_SESSION['points'] >= 5000){
            array_push($headers,"X-Winner: ".$_SESSION['username']);
        }
        curl_setopt($curl,CURLOPT_HTTPHEADER,$headers);
        
        $response = curl_exec($curl);
        echo $response;
        curl_close($curl);
    }


    function httpProxy($query){
        $url = "http://{$_SERVER['SERVER_ADDR']}:8080{$query}";
        $proxyPattern = "@^((?:http:)?)(?://([^/?\#]*))?(.*)$@i";
        preg_match($proxyPattern,$url, $matches);
        list($url,$_shema,$_host,$_uri) = $matches;
        if ($_shema !=='http:'){
            die('Invalid Schema');
        }
        if(validQuery($query) === false){
            die("Invalid Query");
        }
        $invalidProxy = "/(localhost)|(127*)/i";
        if (($_SERVER['SERVER_ADDR'] !== '127.0.0.1') && preg_match($invalidProxy, $_host,$matches)) {
            die("Firewall Blocked");
        }
        $newURL = str_replace("/admin", "", $url);
        return $newURL;
    }

    function validQuery($query) {

        $query = str_replace('+', ' ', $query);

        $query = preg_replace_callback('/%([0-9a-f]{2})/i', function($matches) {
            return chr(hexdec($matches[1]));
        }, $query);


        $validQuery = "@^/admin/(.*)@i";


        if(preg_match($validQuery,$query)){ 
            return true;
        }
        return false;
    }
?>