<html>
 <head>
  <title>Query Results</title>
 </head>
 <body>
 <?php
    $pgc = $_POST['pgc'];

    $ra = $_POST['ra'];
    $dec = $_POST['dec'];
    $region = $_POST['region'];
    // echo $pgc."</br>";
    // var_dump($pgc);
    // echo $ra."</br>";
    // echo $dec."</br>";
    // echo $region."</br>";
    if ($pgc==''){ #is_null doesn't work
    	echo "Search by coordinate around region (degrees)</br>";
	    $db = new PDO('sqlite:rc3.db');
		// $query = "SELECT  ID,PGC_number, ra,dec , radius FROM rc3 WHERE ra BETWEEN 10 AND 11";

		$query = "SELECT   PGC_number, ra,dec , radius,new_ra,new_dec,clean,error FROM rc3 
		WHERE ra  BETWEEN ".(string)($ra-$region)." AND ".(string)($ra+$region).
		" AND dec BETWEEN ".(string)($dec-$region)." AND ".(string)($dec+$region);
		echo "<br>Result for:<br>".$query."<br>";
		$result = $db->prepare($query);
		$result->execute();
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		echo "<tr>";
		// echo "<td>ID</td>";
		echo "<td>PGC_number</td>";
		echo "<td>ra</td>";
		echo "<td>dec</td>";
		echo "<td>radius</td>";
		echo "<td>new_ra</td>";
		echo "<td>new_dec</td>";
		echo "<td>clean</td>";
		echo "<td>error</td>";
		echo "</tr>";
		while($row = $result->fetchObject())
		{  
			// var_dump($row); //used for debugging
		    # Found the error, because inside your query you are only SELECT-ing PGC_number, so you only get PGC_number column that's why the others don't work
		    
			echo "<tr>";
			// echo " <td>".htmlspecialchars($row->ID)."</td>";
			echo " <td>".htmlspecialchars($row->PGC_number)."</td>";
			echo " <td>".htmlspecialchars($row->ra)."</td>";
			echo " <td>".htmlspecialchars($row->dec)."</td>";
			echo " <td>".htmlspecialchars($row->radius)."</td>";
			echo " <td>".htmlspecialchars($row->new_ra)."</td>";
			echo " <td>".htmlspecialchars($row->new_dec)."</td>";
			echo " <td>".htmlspecialchars($row->clean)."</td>";
			echo " <td>".htmlspecialchars($row->error)."</td>";
			echo "</tr>";

		}
		echo "<table>";
    }else{
    	echo "Search by PGC number </br>";
	    $db = new PDO('sqlite:rc3.db');
		// $query = "SELECT  ID,PGC_number, ra,dec , radius FROM rc3 WHERE ra BETWEEN 10 AND 11";
		$query = "SELECT   PGC_number, ra,dec , radius FROM rc3 WHERE PGC_number = $pgc ";
		$result = $db->prepare($query);
		$result->execute();
		echo "<br>Result for:<br>".$query."<br>";
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		echo "<tr>";
		// echo "<td>ID</td>";
		echo "<td>PGC_number</td>";
		echo "<td>ra</td>";
		echo "<td>dec</td>";
		echo "<td>Radius</td>";
		echo "</tr>";
		while($row = $result->fetchObject())
		{  
			// var_dump($row); //used for debugging
		    # Found the error, because inside your query you are only SELECT-ing PGC_number, so you only get PGC_number column that's why the others don't work
		    
			echo "<tr>";
			// echo " <td>".htmlspecialchars($row->ID)."</td>";
			echo " <td>".htmlspecialchars($row->PGC_number)."</td>";
			echo " <td>".htmlspecialchars($row->ra)."</td>";
			echo " <td>".htmlspecialchars($row->dec)."</td>";
			echo " <td>".htmlspecialchars($row->radius)."</td>";
			echo "</tr>";

		}
		echo "<table>";
    }

	// echo "End Connection with MySQL<br>";

 ?>

 </body>
</html>





