''' 
This script merges the data product output 
[pgc_number]-->[files] from each survey 
to the general catalog format 
[pgc_number]-->dss,sdss,2mass..etc-->[files]
'''
import os
import shutil
ADDITIONAL_NUM_DSS_COUNT =0
for i in os.listdir("dss_data/"):
	print i 
	if os.path.exists("rc3/{}".format(i)):
		#object already exist (covered by other surveys), just copy the dss directory there		
		pass
	else:
		# object doesn't exist, start a new survey
		ADDITIONAL_NUM_DSS_COUNT +=1
		#Actually the directory structure is [pgc_number]-->[files] so I need to create dss folder
		os.mkdir("dss")
		for j in glob.glob("rc3/{}/*".format(i)):                                                                                                                                      
			shutil.copy(j, "dss")
		os.mkdir("rc3/{}".format(i))
	shutil.move("dss_data/{}".format(i), "rc3/{}/".format(i))
print ADDITIONAL_NUM_DSS_COUNT
