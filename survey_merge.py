'''
This script merges the data product output
[pgc_number]-->[files] from each survey
to the general catalog format
[pgc_number]-->dss,sdss,2mass..etc-->[files]
'''
import os
import glob
import shutil
ADDITIONAL_NUM_DSS_COUNT =0
# for i in os.listdir("dss_data/"):
# eliminate weird files like .DSStore and other php and html files
for i in [name for name in os.listdir("dss_data") if os.path.isdir(os.path.join("dss_data", name)) ]:
     print i
     if os.path.exists("rc3/{}".format(i)):
          #object already exist (covered by other surveys), just copy the dss directory there        
          os.mkdir("dss_data/dss")
          for j in glob.glob("dss_data/{}/*".format(i)):
               shutil.copy(j, "dss_data/dss")
          shutil.move("dss_data/dss", "rc3/{}/".format(i))
     else:
          # object doesn't exist, start a new survey
          ADDITIONAL_NUM_DSS_COUNT +=1
          #Actually the directory structure is [pgc_number]-->[files] so I need to create dss folder
          os.mkdir("dss_data/dss")
          for j in glob.glob("dss_data/{}/*".format(i)):
               shutil.copy(j, "dss_data/dss")
          os.mkdir("rc3/{}".format(i))
          shutil.move("dss_data/dss", "rc3/{}/".format(i))
print ADDITIONAL_NUM_DSS_COUNT