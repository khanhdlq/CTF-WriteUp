<?php
    session_start();
    require_once "config.php";
    header("Content-Type: application/json");
    if(($_SERVER['REMOTE_ADDR'] === '127.0.0.1' || $_SERVER['REMOTE_ADDR'] === '::1')) {
        $accessToken = apache_request_headers()['X-Access-Token'];
        list($username,$password) = explode(":",base64_decode($accessToken));

        if(isAdmin($conn,$username, $password)) {
            if($_POST['action'] == "update"){

                if(isset($_POST["username"]) && $_POST["points"]){

                    try {
                        $query = "UPDATE users SET points = :points WHERE username = :username AND role = 'user'";
                        // Prepare and execute a SQL statement
                        $stmt = $conn->prepare($query);
                        $stmt->bindParam(':username', $_POST['username'], PDO::PARAM_STR);
                        $stmt->bindParam(':points', $_POST['points'], PDO::PARAM_STR);
                        if($stmt->execute() && $stmt->rowCount() > 0) {
                            echo json_encode(array("success" => true));
                        }else{
                            echo json_encode(array("success" => false));
                        };
                    } catch (PDOException $e) {

                        // echo 'Query failed';
                        echo 'Query failed: ' . $e->getMessage();
                    }
                }
            }
        }
        else{
            die('Admin access only');
        }
    }
    else{
        die("Firewall blocked");
    }
    function isAdmin( $conn, $username , $password) {
        try {
            $query = "SELECT userId FROM users WHERE username = :username AND password = :password and role = 'admin'";
            // Prepare and execute a SQL statement
            $stmt = $conn->prepare($query);
            $stmt->bindParam(':username', $username, PDO::PARAM_STR);
            $stmt->bindParam(':password', $password, PDO::PARAM_STR);
            $stmt->execute();
            if($stmt->rowCount() > 0){
                return true;
            }
            return false;
        } catch (PDOException $e) {
            // echo 'Query failed';
            // echo 'Query failed: ' . $e->getMessage();
        }
    }
?>