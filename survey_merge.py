''' 
This script merges the data product output 
[pgc_number]-->dss-->[files] from each survey 
to the general catalog format 
[pgc_number]-->dss,sdss,2mass..etc-->[files]
'''
import os
import shutil
NUM_DSS_IN_SDSS_COUNT =0
for i in os.listdir("dss/"):
	print i 
	if os.path.exists("rc3/{}".format(i)):
		#object already exist (covered by other surveys), just copy the dss directory there
		NUM_DSS_IN_SDSS_COUNT +=1
		shutil.move("dss/{}".format(i), "rc3/{}".format(i))
