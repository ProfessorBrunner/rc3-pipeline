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
		$query = "SELECT  * FROM rc3 
		WHERE new_ra  BETWEEN ".(string)($ra-$region)." AND ".(string)($ra+$region).
		" AND new_dec BETWEEN ".(string)($dec-$region)." AND ".(string)($dec+$region);
		echo "<br>Result for:<br>".$query."<br>";
		$result = $db->prepare($query);
		$result->execute();
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		echo "<tr>";
                echo "<td>PGC</td>";
                echo "<td>rc3_ra</td>";
                echo "<td>rc3_dec</td>";
                echo "<td>rc3_radius</td>";
                echo "<td>new_ra</td>";
                echo "<td>new_dec</td>";
                echo "<td>clean</td>";
                echo "<td>error</td>";
                echo "<td>in SDSS footprint</td>";
                echo "<td>Low surface structure image</td>";
                echo "<td>Poster image</td>";
                echo "<td>ufits</td>";
                echo "<td>gfits</td>";
                echo "<td>rfits</td>";
                echo "<td>ifits</td>";
                echo "<td>zfits</td>";
                echo "</tr>";
		while($row = $result->fetchObject())
		{  
			// var_dump($row); //used for debugging
                        echo "<tr>";
                        echo " <td>".htmlspecialchars($row->PGC)."</td>";
                        echo " <td>".htmlspecialchars($row->rc3_ra)."</td>";
                        echo " <td>".htmlspecialchars($row->rc3_dec)."</td>";
                        echo " <td>".htmlspecialchars($row->rc3_radius)."</td>";
                        echo " <td>".htmlspecialchars($row->new_ra)."</td>";
                        echo " <td>".htmlspecialchars($row->new_dec)."</td>";
                        echo " <td>".htmlspecialchars($row->clean)."</td>";
                        echo " <td>".htmlspecialchars($row->error)."</td>";
                        echo " <td>".htmlspecialchars($row->in_SDSS_footprint)."</td>";
                        //echo " <td><form><input type='button' value='Download' onClick='window.location.href='".htmlspecialchars($row->best)."''></form></td>";
                         //echo "<td><form><input type='button' value='Download' onClick='window.location.href='/Library/WebServer/Documents/data/rc3/search.html''></form></td>";
                        //echo "<td><a href='/Library/WebServer/Documents/data/rc3/search.html' target='_blank'>Download</a></td>";
//                      $pieces = explode("/", htmlspecialchars($row->best));
                        echo "<td><a href='".htmlspecialchars($row->low)."' target='_blank'>".explode("/", htmlspecialchars($row->low))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->best)."' target='_blank'>".explode("/", htmlspecialchars($row->best))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->ufits)."' target='_blank'>".explode("/", htmlspecialchars($row->ufits))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->gfits)."' target='_blank'>".explode("/", htmlspecialchars($row->gfits))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->rfits)."' target='_blank'>".explode("/", htmlspecialchars($row->rfits))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->ifits)."' target='_blank'>".explode("/", htmlspecialchars($row->ifits))[6]."</a></td>";
                        echo "<td><a href='".htmlspecialchars($row->zfits)."' target='_blank'>".explode("/", htmlspecialchars($row->zfits))[6]."</a></td>";
                        echo "</tr>";
		}
		echo "<table>";
echo "Note: Query result of RC3 galaxies are based updated position values instead of values recorded in the RC3 Catalog";
    }else{
    	echo "Search by PGC number </br>";
	    $db = new PDO('sqlite:rc3.db');
		//$query = "SELECT   PGC, rc3_ra,rc3_dec , rc3_radius,new_ra,new_dec,new_radius,ufits,gfits,rfits,ifits,zfits ,low,best ,in_SDSS_footprint,clean ,error FROM rc3 WHERE PGC= $pgc ";
		$query = "SELECT *FROM rc3 WHERE PGC= $pgc ";
		$result = $db->prepare($query);
		$result->execute();
		echo "<br>Result for:<br>".$query."<br>";
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		
                echo "<tr>";
                // echo "<td>ID</td>";
                echo "<td>PGC</td>";
                echo "<td>rc3_ra</td>";
                echo "<td>rc3_dec</td>";
                echo "<td>rc3_radius</td>";
                echo "<td>new_ra</td>";
                echo "<td>new_dec</td>";
                echo "<td>clean</td>";
                echo "<td>error</td>";
                echo "<td>in SDSS footprint</td>";
                echo "<td>Low surface structure image</td>";
                echo "<td>Poster image</td>";
                echo "<td>ufits</td>";
                echo "<td>gfits</td>";
                echo "<td>rfits</td>";
                echo "<td>ifits</td>";
                echo "<td>zfits</td>";
                echo "</tr>";
		while($row = $result->fetchObject())
		{  
			// var_dump($row); //used for debugging
		    # Found the error, because inside your query you are only SELECT-ing PGC_number, so you only get PGC_number column that's why the others don't work
		    
			echo "<tr>";
			echo " <td>".htmlspecialchars($row->PGC)."</td>";
			echo " <td>".htmlspecialchars($row->rc3_ra)."</td>";
			echo " <td>".htmlspecialchars($row->rc3_dec)."</td>";
			echo " <td>".htmlspecialchars($row->rc3_radius)."</td>";
			echo " <td>".htmlspecialchars($row->new_ra)."</td>";
			echo " <td>".htmlspecialchars($row->new_dec)."</td>";
			echo " <td>".htmlspecialchars($row->clean)."</td>";
			echo " <td>".htmlspecialchars($row->error)."</td>";
			echo " <td>".htmlspecialchars($row->in_SDSS_footprint)."</td>";
			//echo " <td><form><input type='button' value='Download' onClick='window.location.href='".htmlspecialchars($row->best)."''></form></td>"; 
			 //echo "<td><form><input type='button' value='Download' onClick='window.location.href='/Library/WebServer/Documents/data/rc3/search.html''></form></td>";
			//echo "<td><a href='/Library/WebServer/Documents/data/rc3/search.html' target='_blank'>Download</a></td>";
//			$pieces = explode("/", htmlspecialchars($row->best));
			echo "<td><a href='".htmlspecialchars($row->low)."' target='_blank'>".explode("/", htmlspecialchars($row->low))[6]."</a></td>";
			echo "<td><a href='".htmlspecialchars($row->best)."' target='_blank'>".explode("/", htmlspecialchars($row->best))[6]."</a></td>";
			echo "<td><a href='".htmlspecialchars($row->ufits)."' target='_blank'>".explode("/", htmlspecialchars($row->ufits))[6]."</a></td>";
			echo "<td><a href='".htmlspecialchars($row->gfits)."' target='_blank'>".explode("/", htmlspecialchars($row->gfits))[6]."</a></td>";
			echo "<td><a href='".htmlspecialchars($row->rfits)."' target='_blank'>".explode("/", htmlspecialchars($row->rfits))[6]."</a></td>";
			echo "<td><a href='".htmlspecialchars($row->ifits)."' target='_blank'>".explode("/", htmlspecialchars($row->ifits))[6]."</a></td>";
 			echo "<td><a href='".htmlspecialchars($row->zfits)."' target='_blank'>".explode("/", htmlspecialchars($row->zfits))[6]."</a></td>";
			echo "</tr>";

		}
		echo "<table>";
    }

	// echo "End Connection with MySQL<br>";

 ?>

 </body>
</html>





