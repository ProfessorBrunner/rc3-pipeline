<html>
<head>
<meta http-equiv="Content-Type" content="text/html">
<title>RC3 Gallery</title>
<style type="text/css">
body {
    margin: 0 auto 20px;
    padding: 0;
    background: #ffffff;
    text-align: center;
}
td {
    padding: 0 0 50px;
    text-align: center;
    font: 9px sans-serif;
}
table {
    width: 100%;
}
img {
    display: block;
    margin: 20px auto 10px;
    max-width: 900px;
    outline: none;
}
img:active {
    max-width: 100%;
}
a:focus {
    outline: none;
}
</style>
</head>
<body>

<form action="pgc.php" target='_blank' method="post">
Search by PGC number :
<br/>
<input type="text" name="pgc" />
<br/>
<input type="submit" name="submit" value="Submit" />
<br/>

<?php
$folder = 'img/';
$filetype = '*.*';
$files = glob($folder.$filetype);
$count = count($files);
echo '<table>';
$n=0;

for ($i = 0; $i < $count; $i++) {
    $fname = substr($files[$i],strlen($folder),strpos($files[$i], '.')-strlen($folder));
    $pgc = explode("_", $fname);
    #echo $pgc[1];
    #echo '<a href="pgc.php?pgc='.$pgc[1].'">'.$pgc[1].'</a>';
    if ($n>=4){ 
        echo '<td>'.$fname.'<a name="'.$i.'" href="pgc.php?pgc='.$pgc[1].'"><img src="'.$files[$i].'" /></a></td>';
        $n=0;
        echo '</tr>';
    }elseif($n==0){
        echo '<tr>';
        echo '<td>'.$fname.'<a name="'.$i.'" href="pgc.php?pgc='.$pgc[1].'"><img src="'.$files[$i].'" /></a></td>';
        $n=$n+1;
    }else{
        echo '<td>'.$fname.'<a name="'.$i.'" href="pgc.php?pgc='.$pgc[1].'"><img src="'.$files[$i].'" /></a></td>';
        $n=$n+1;
    }

}
echo '</table>';
?>