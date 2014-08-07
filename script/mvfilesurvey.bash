for SUBDIR in `find SDSS_run_result  -maxdepth 1 -type d | tail -n +2` ;
do
    OBJA="${SUBDIR}/sdss"
    mkdir -p $OBJA
    for j in `find $SUBDIR -maxdepth 1 | tail -n +2` ;
    do
            echo $j
            mv  $j $OBJA 
    done
done
