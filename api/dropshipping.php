<?php
header("Content-Type: application/json; charset=UTF-8");
$json_data = file_get_contents('../data/dropshipping.json');
echo $json_data;
?>
