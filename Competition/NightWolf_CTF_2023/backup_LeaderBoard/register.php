<?php
session_start();

require_once ("../admin/config.php");
if (isset($_POST['name']) && isset($_POST['username']) && isset($_POST['password']))
{
    if (preg_match('/^[a-zA-Z0-9\s]+$/', $_POST['name']))
    {
        $name = $_POST['name'];
    }
    else
    {
        die('Invalid name');
    }
    if (preg_match('/^[a-zA-Z0-9_]+$/', $_POST['username']))
    {
        if (isDuplicate($conn, $_POST['username']))
        {
            $username = $_POST['username'];
        }

    }
    else
    {
        die('Invalid username');
    }
    if (preg_match("/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/", $_POST['password']))
    {
      $password = $_POST['password'];
    }
    else
    {
        die('Weak password, enter a stronger password');
    }
    $points = random_int(300, 3000);
    try
    {
        $query = "INSERT INTO users (name, username,password, points, role) VALUES(:name,:username,:password,:points,'user');";

        $stmt = $conn->prepare($query);

        $stmt->bindParam(':name', $name, PDO::PARAM_STR);
        $stmt->bindParam(':username', $username, PDO::PARAM_STR);
        $stmt->bindParam(':password', $password, PDO::PARAM_STR);
        $stmt->bindParam(':points', $points, PDO::PARAM_INT);

        $stmt->execute();
        // echo "Record inserted successfully";
        
    }
    catch(PDOException $e)
    {
        // echo "Error: " . $e->getMessage();
        
    }
}
function isDuplicate($conn, $username)
{
    try
    {

        // Username to check for duplicates
        // Check if the username already exists
        $stmt = $conn->prepare("SELECT userId FROM users WHERE username = :username");
        $stmt->bindParam(':username', $username, PDO::PARAM_STR);
        $stmt->execute();

        $count = $stmt->rowCount(); // Count the number of rows
        if ($count > 0)
        {
            die("Username already exists.");
        }

    }
    catch(PDOException $e)
    {
        // echo "Error: " . $e->getMessage();
        
    }
    return true;
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Register</title>
  <link rel="stylesheet" href="css/register.css">
</head>

<body>
  <div class="register-container">
    <h1>Register</h1>
    <form method="POST">
      <div class="form-group">
        <label for="name">Fullname:</label>
        <input type="text" class="form-control" id="name" name="name" placeholder="Fullname" required>
      </div>
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" class="form-control" id="username" name="username" placeholder="Username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</body>

</html>