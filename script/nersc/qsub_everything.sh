for i in $( ls -d RUN* );do qsub $i/run.pbs ;done
