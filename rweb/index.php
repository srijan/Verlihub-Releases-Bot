<?php include "includes/header.php"; ?>
<?php include "includes/sidebar.php"; ?>
<?php

/**
 * Convert bytes to human readable format
 *
 * @param integer bytes Size in bytes to convert
 * @return string
 */
function bytesToSize($bytes, $precision = 2) {
  $kilobyte = 1024;
  $megabyte = $kilobyte * 1024;
  $gigabyte = $megabyte * 1024;
  $terabyte = $gigabyte * 1024;

  if (($bytes >= 0) && ($bytes < $kilobyte)) {
    return $bytes . ' B';

  } elseif (($bytes >= $kilobyte) && ($bytes < $megabyte)) {
    return round($bytes / $kilobyte, $precision) . ' KB';

  } elseif (($bytes >= $megabyte) && ($bytes < $gigabyte)) {
    return round($bytes / $megabyte, $precision) . ' MB';

  } elseif (($bytes >= $gigabyte) && ($bytes < $terabyte)) {
    return round($bytes / $gigabyte, $precision) . ' GB';

  } elseif ($bytes >= $terabyte) {
    return round($bytes / $terabyte, $precision) . ' TB';
  } else {
    return $bytes . ' B';
  }
}

?>
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
              ORDER BY `added_at` DESC";
    $result_set = mysql_query($query);
    if(mysql_num_rows($result_set) > 0) {
      echo "
        <tr>
          <th colspan='3'>".$category['name']."</th>
        </tr>";
      while($result = mysql_fetch_array($result_set)) {
        if(substr($result['text'],0,8) == "magnet:?") {
          parse_str($result['text']);
          $text = "<a href='".$result['text']."'>".$dn." (".bytesToSize($xl).")</a>";
        }
        else {
          $text = $result['text'];
        }
        echo "
          <tr>
            <td>".$result['id']."</td>
            <td>".$text."</td>
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
