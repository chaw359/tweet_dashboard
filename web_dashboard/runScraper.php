<?php 

$command = escapeshellcmd('main.py '.$_POST["user"]);
shell_exec($command);

?>