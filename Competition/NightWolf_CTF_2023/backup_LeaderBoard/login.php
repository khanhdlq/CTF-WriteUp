<?php
// Set error reporting to E_ERROR only
require_once ("config.php");
session_start();
if (isset($_POST['username']) && isset($_POST['password']))
{
    try
    {
        $query = "SELECT userId, points, username, password,role FROM users WHERE username = :username and password = :password";
        $stmt = $conn->prepare($query);
        $stmt->bindParam(':username', $_POST['username'], PDO::PARAM_STR);
        $stmt->bindParam(':password', $_POST['password'] , PDO::PARAM_STR);

        $stmt->execute();
        if ($stmt->rowCount() > 0)
        {
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            $_SESSION['userId'] = $row['userId'];
            $_SESSION['username'] = $row['username'];
            $_SESSION['points'] = $row['points'];
            $_SESSION['password'] = $row['password'];
            header('Location: leaderboard.php');
        }
        else
        {
            die('Login failed');
        }

        // echo "Record inserted successfully";
        
    }
    catch(PDOException $e)
    {
        // echo "Error: " . $e->getMessage();
        
    }
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login</title>
  <link rel="stylesheet" href="css/login.css">
</head>
<body>
  <div class="login-container">
    <h1>Login</h1>
    <form method="POST">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" class="form-control" id="username" name="username" placeholder="Username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</body>
</html>