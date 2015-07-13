import sys
#nproc is not npric here, it is a dummy for just the number of run counts
for arg in sys.argv: 
    nproc=arg
nproc = int(nproc)
print "#PBS -q thruput"
print "#PBS -l mppwidth=1"
print "#PBS -l walltime=168:00:00"
print "#PBS -N RC3_RUN{}".format(nproc)
print "#PBS -e test.$PBS_JOBID.err"
print "#PBS -o test.$PBS_JOBID.out"
print "#PBS -A m2218"
print "source /project/projectdirs/cmb/modules/hpcports_NERSC.sh"
print "hpcports shared_gnu"
print "module load astromatic-hpcp"
print "module load python"
print "cd $GSCRATCH/rc3/RUN{}".format(nproc)
print "aprun -n 1 python bulk_run.py" 
