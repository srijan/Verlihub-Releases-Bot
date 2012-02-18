  <div id="sidebar">
    <ul>
      <li><a href="index.php">[ ALL ]</a></li>
<?php
require_once "includes/constants.php";
$connection = mysql_connect(DB_SERVER,DB_USER,DB_PASS);

if(!$connection) {
  die("Database connection failed: " . mysql_error());
}

$db_select = mysql_select_db(DB_NAME,$connection);
if(!$db_select) {
  die("Database selection failed: " . mysql_error());
}
$query = "SELECT `name` FROM `pi_rel_categories`";
$categories_set = mysql_query($query);

while($category = mysql_fetch_array($categories_set)) {
  echo"<li><a href='index.php?p=".$category['name']."'>[ ".$category['name']." ]</a></li>";
}

?>
      <li><a href="about.php">[ about ]</a></li>
    </ul>
  </div>
