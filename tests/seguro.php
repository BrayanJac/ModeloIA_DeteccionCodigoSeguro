<?php

$user = $_GET['user'];

$stmt = $db->prepare(
    "SELECT * FROM users WHERE username = ?"
);

$stmt->execute([$user]);

?>