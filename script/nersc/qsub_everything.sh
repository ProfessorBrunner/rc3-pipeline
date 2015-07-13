for i in $( ls -d RUN* );do qsub $i/run.pbs ;done
#qhold everything
#for i in $(seq 66 75); do qhold 95729$i.hopque01 ;done
