<html>
 <head>
  <title>Query Results Page</title>
 </head>
 <body>
 <?php
    $ra = $_POST['ra'];
    $dec = $_POST['dec'];
    $region = $_POST['region'];
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
        echo "<td><a href='".htmlspecialchars($row->low)."'download='".htmlspecialchars($row->low)."' target='_blank'>".explode("/", htmlspecialchars($row->low))[2]."</a></td>";
        echo "<td><a href='".htmlspecialchars($row->best)."'download='".htmlspecialchars($row->best)."' target='_blank'>".explode("/", htmlspecialchars($row->best))[2]."</a></td>";
        echo "<td><a href='".htmlspecialchars($row->ufits)."'download='".htmlspecialchars($row->ufits)."' target='_blank'>".explode("/", htmlspecialchars($row->ufits))[2]."</a></td>";
        echo "<td><a href='".htmlspecialchars($row->gfits)."'download='".htmlspecialchars($row->gfits)."' target='_blank'>".explode("/", htmlspecialchars($row->gfits))[2]."</a></td>";
        echo "<td><a href='".htmlspecialchars($row->rfits)."'download='".htmlspecialchars($row->rfits)."' target='_blank'>".explode("/", htmlspecialchars($row->rfits))[2]."</a></td>";
        echo "<td><a href='".htmlspecialchars($row->ifits)."'download='".htmlspecialchars($row->ifits)."' target='_blank'>".explode("/", htmlspecialchars($row->ifits))[2]."</a></td>";        
        echo "<td><a href='".htmlspecialchars($row->zfits)."'download='".htmlspecialchars($row->zfits)."' target='_blank'>".explode("/", htmlspecialchars($row->zfits))[2]."</a></td>";
        echo "</tr>";
	}
	echo "<table>";
    echo "Note: Query result of RC3 galaxies are based updated position values instead of values recorded in the RC3 Catalog";
 ?>

 </body>
</html>





