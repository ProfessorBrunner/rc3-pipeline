source /project/projectdirs/cmb/modules/hpcports_NERSC.sh
hpcports shared_gnu
module load astromatic-hpcp
module load python
line=2612 #starting from line 2612
step=2400 #Estimated number of lines that the pipeline goes thorugh in 48 hour runs  (!= to # of galaxy mosaiced!)
for (( i=1; i <=10; i++ ))
 do
   line=$[$line+$step] 
   dir="RUN$i"
   echo $dir
   cp -r  pipeline/ $dir
   cd $dir
   #Call python script that generates output of new run.pbs
   python ../getserialscript.py $i > run.pbs
   # Call python script that modifies where the starting point in rc3_ra_dec_diameter_pgc.txt
   python ../insert_start.py $i $line  
   echo "Submitting RUN$i"
   qsub.serial run.pbs
   cd .. 
done
