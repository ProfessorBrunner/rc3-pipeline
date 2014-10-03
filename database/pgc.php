<html>
 <head>
  <title>Query Results Page</title>
 </head>
 <body>
 <?php
    // $pgc = $_POST['pgc'];
    $pgc=$_GET["pgc"];
    $survey=$_GET["survey"];
    //echo $survey;
    if ($survey=="sdss"){
	echo "Search by PGC number </br>";
    	$db = new PDO('sqlite:rc3.db');
	$query = "SELECT *FROM rc3 WHERE PGC= $pgc ";
	$result = $db->prepare($query);
	$result->execute();
	echo "<br>Result for:<br>".$query."<br>";
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
	    echo "</tr>";
	    while($row = $result->fetchObject())
	    {  
			    
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
		echo "</tr>";
		echo "<table>";
		echo "</br> Downloads </br>";
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		echo "<tr>";
		echo "<td>ufits</td>";
		echo "<td>gfits</td>";
		echo "<td>rfits</td>";
		echo "<td>ifits</td>";
		echo "<td>zfits</td>";
                echo "<td>Low surface structure image</td>";
                echo "<td>Poster image</td>";
		echo "</tr>";
		echo "<tr>";
		echo "<td><a href='".htmlspecialchars($row->ufits)."'download='".htmlspecialchars($row->ufits)."' target='_blank'>".explode("/", htmlspecialchars($row->ufits))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->gfits)."'download='".htmlspecialchars($row->gfits)."' target='_blank'>".explode("/", htmlspecialchars($row->gfits))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->rfits)."'download='".htmlspecialchars($row->rfits)."' target='_blank'>".explode("/", htmlspecialchars($row->rfits))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->ifits)."'download='".htmlspecialchars($row->ifits)."' target='_blank'>".explode("/", htmlspecialchars($row->ifits))[5]."</a></td>";        
		echo "<td><a href='".htmlspecialchars($row->zfits)."'download='".htmlspecialchars($row->zfits)."' target='_blank'>".explode("/", htmlspecialchars($row->zfits))[5]."</a></td>";
echo "<td><a href='".htmlspecialchars($row->low)."'download='".htmlspecialchars($row->low)."' target='_blank'>".explode("/", htmlspecialchars($row->low))[5]."</a></td>";
                echo "<td><a href='".htmlspecialchars($row->best)."'download='".htmlspecialchars($row->best)."' target='_blank'>".explode("/", htmlspecialchars($row->best))[5]."</a></td>";
		echo "</tr>";

	    }
	    echo "<table>";
   }
  else if ($survey=="dss"){
	echo "Search by PGC number </br>";
    	$db = new PDO('sqlite:rc3_dss.db');
	$query = "SELECT *FROM rc3 WHERE PGC= $pgc ";
	$result = $db->prepare($query);
	$result->execute();
	echo "<br>Result for:<br>".$query."<br>";
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
	    echo "<td>in DSS footprint</td>";
	    echo "</tr>";
	    while($row = $result->fetchObject())
	    {  
			    
		echo "<tr>";
		echo " <td>".htmlspecialchars($row->PGC)."</td>";
		echo " <td>".htmlspecialchars($row->rc3_ra)."</td>";
		echo " <td>".htmlspecialchars($row->rc3_dec)."</td>";
		echo " <td>".htmlspecialchars($row->rc3_radius)."</td>";
		echo " <td>".htmlspecialchars($row->new_ra)."</td>";
		echo " <td>".htmlspecialchars($row->new_dec)."</td>";
		echo " <td>".htmlspecialchars($row->clean)."</td>";
		echo " <td>".htmlspecialchars($row->error)."</td>";
		echo " <td>".htmlspecialchars($row->in_DSS_footprint)."</td>";
		echo "</tr>";
		echo "<table>";
		echo "</br> Downloads </br>";
		echo "<br><table style='width:300px' border='1' cellpadding='10px'>  ";
		echo "<tr>";
		echo "<td>1Bfits</td>";
		echo "<td>1Rfits</td>";
		echo "<td>2Bfits</td>";
		echo "<td>2Rfits</td>";
		echo "<td>2IRfits</td>";
                echo "<td>Low surface structure image</td>";
                echo "<td>Poster image</td>";
		echo "</tr>";
		echo "<tr>";
		echo "<td><a href='".htmlspecialchars($row->b1)."'download='".htmlspecialchars($row->ufits)."' target='_blank'>".explode("/", htmlspecialchars($row->b1))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->r1)."'download='".htmlspecialchars($row->gfits)."' target='_blank'>".explode("/", htmlspecialchars($row->r1))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->b2)."'download='".htmlspecialchars($row->rfits)."' target='_blank'>".explode("/", htmlspecialchars($row->b2))[5]."</a></td>";
		echo "<td><a href='".htmlspecialchars($row->r2)."'download='".htmlspecialchars($row->ifits)."' target='_blank'>".explode("/", htmlspecialchars($row->r2))[5]."</a></td>";        
		echo "<td><a href='".htmlspecialchars($row->ir2)."'download='".htmlspecialchars($row->zfits)."' target='_blank'>".explode("/", htmlspecialchars($row->ir2))[5]."</a></td>";
                echo "<td><a href='".htmlspecialchars($row->low)."'download='".htmlspecialchars($row->low)."' target='_blank'>".explode("/", htmlspecialchars($row->low))[5]."</a></td>";
                echo "<td><a href='".htmlspecialchars($row->best)."'download='".htmlspecialchars($row->best)."' target='_blank'>".explode("/", htmlspecialchars($row->best))[5]."</a></td>";
		echo "</tr>";

	    }
	    echo "<table>";
   }

 ?>

 </body>
</html>





