<?php
session_start();
$command = escapeshellcmd('/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/gfuccio/GitHub/tweet_dashboard/main.py '.$_POST["user"]);
shell_exec($command);
$_SESSION['username'] = $_POST['user'];
echo "Redirecting to dashboard...";

header('location:http://localhost/web_dashboard/dashboard.html');
?>
