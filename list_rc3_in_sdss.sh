for i in */
  do 
    if [ -d $i/sdss/ ]; then
	echo $i    
	echo $i | cut -f1 -d'/'>> rc3_in_sdss.txt
    fi
  done
