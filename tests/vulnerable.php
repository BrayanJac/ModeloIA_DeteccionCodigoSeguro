<?php

$user = $_GET['user'];

$sql =
"SELECT * FROM users WHERE username='$user'";

$result = $db->query($sql);

?>