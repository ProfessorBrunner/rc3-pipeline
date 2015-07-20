for i in RUN*
  do
    echo "Working on $i"
    cd $i
    ls -d */ | cut -f1 -d'/' >> ../pgc_done.txt
    cd ..
  done
