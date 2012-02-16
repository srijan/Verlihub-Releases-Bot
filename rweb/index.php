<?php include "includes/header.php"; ?>
<?php include "includes/sidebar.php"; ?>
  <div id="content">
    <h2>[ All Releases ]</h2>
<?php if(isset($_GET['message'])) {
  echo "<p class = \"message\">".$_GET['message']."</p>";
} ?>

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

  echo "
    <table id='gradient-style' summary='Releases List'>
      <thead>
        <tr>
          <th scope='col'>ID</th>
          <th scope='col'>Release</th>
          <th scope='col'>Downloader</th>
        </tr>
      </thead>
      <tbody>
      ";

  while($category = mysql_fetch_array($categories_set)) {
    $query = "SELECT `id`,`text`,`added_by`
              FROM `pi_releases`
              WHERE `category`='".$category['name']."'
              ORDER BY `added_at`";
    $result_set = mysql_query($query);
    if(mysql_num_rows($result_set) > 0) {
      echo "
        <tr>
          <th colspan='3'>".$category['name']."</th>
        </tr>";
      while($result = mysql_fetch_array($result_set)) {
        echo "
          <tr>
            <td>".$result['id']."</td>
            <td>".$result['text']."</td>
            <td>".$result['added_by']."</td>
          </tr>";
      }
    }
  }
  echo "
      </tbody>
    </table>
    ";
  mysql_close();

?>

  </div>
<?php include "includes/footer.php"; ?>
