<?php include "includes/header.php"; ?>
<?php include "includes/sidebar.php"; ?>
  <div id="content">
    <h2>[ home ]</h2>
<?php if(isset($_GET['message'])) {
  echo "<p class = \"message\">".$_GET['message']."</p>";
} ?>
    <p>Releases BOT is a python bot script written for managing releases for Verlihub.</p>
  </div>
<?php include "includes/footer.php"; ?>
