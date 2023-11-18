<?php

require_once ("config.php");
session_start();

try
{
    $query = "SELECT name, points, username FROM users ";
    $where .= "WHERE role = 'user' ";
    $orderBy = "ORDER BY ";
    if (!empty($_GET['search']))
    {
        $search = '%' . $_GET['search'] . '%';
        $where .= "AND (name LIKE :search OR username LIKE :search) ";
    }
    if (!empty($_GET['orderBy']))
    {
        if (preg_match('/\s/', $_GET['orderBy'])) die('Firewall blocked'); // no whitespaces
        if (preg_match('/[\'"]/', $_GET['orderBy'])) die('Firewall blocked'); // no quotes
        if (preg_match('/[\/\\\\]/', $_GET['orderBy'])) die('Firewall blocked'); // no slashes
        if (preg_match('/(and|sub|if|cast)/i', $_GET['orderBy'])) die('Firewall blocked'); // no sqli keywords
        if (preg_match('/(;|--|#|\/\*)/', $_GET['orderBy'])) die('Firewall blocked'); // no sqli keywords
        $orderBy .= $_GET['orderBy'];
    }
    else
    {
        $orderBy .= 'points ';
    }
    if (!empty($_GET['order']) && in_array(strtoupper($_GET['order']) , array('ASC','DESC')))
    {
        $orderBy .= " {$_GET['order']}";
    }
    else
    {
        $orderBy .= " DESC";
    }
    substr($_GET['orderBy'], strrpos($_GET['orderBy'], ',') + 1);
    $finalQuery = $query . $where . $orderBy . " LIMIT 20";
    $stmt = $conn->prepare($finalQuery);
    $stmt->bindParam(':search', $search, PDO::PARAM_STR);

    $stmt->execute();
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
    // echo "Record inserted successfully";
    
}
catch(PDOException $e)
{
    // echo "Error: " . $e->getMessage();
}

?>


<!DOCTYPE html>
<html>

<head>
  <title>FPT Software Leaderboard</title>
  <link rel="stylesheet" type="text/css" href="css/styles.css">
</head>

<body>
  <div class="container">
    <h1>FPT Software Leaderboard</h1>
    <div class="search-container">
      <form method="GET" class="search-form">
        <input type="text" id="search" name="search" placeholder="Search player...">
      </form>
    </div>
    <table id="user-table">
      <tr>
        <th>Player</th>
        <th>Points</th>
      </tr>
      <?php if ($results != NULL) {
        foreach ($results as $row) { ?>
          <tr>
            <td>
              <?= $row['name'] ?> (<?= $row['username'] ?>)
            </td>
            <td>
              <?= $row['points'] ?>
            </td>
          </tr>
        <?php }
      } ?>
    </table>
  </div>
</body>

</html>