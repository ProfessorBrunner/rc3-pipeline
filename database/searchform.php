<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
 <?php echo '<p>Hello World</p>'; ?> 
 <?php  
	//connection to the database
	$dbhandle = mysqli_connect();
	echo "Connected to MySQL<br>";
 ?>
 </body>
</html>