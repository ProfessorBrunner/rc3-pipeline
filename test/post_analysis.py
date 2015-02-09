#Analysis Script: 
# Running SExtractor on 
# Checking Astrometry
# Conduct all our analysis on r band
import numpy as np
import glob
import os
import shutil
import matplotlib.pyplot as plt
PGC = 250
for i in glob.glob("default.*"):
    shutil.copy(i,"{}/".format(PGC))
os.chdir(str(PGC))
os.system("sex  SDSS_r_{}r.fits".format(PGC))
os.rename("test.cat","output.cat") #rename it more appropriately as output catalog
# with open("output.txt",'r') as f:
#     for line in f:
#         print ()
#-------------------------------------#

for i in glob.glob("default.*"):
    shutil.copy(i,"{}/".format("r"))
os.chdir("r")
all_r_input = glob.glob("raw/frame-*")
os.system("sex  {}".format(all_r_input[0]))
os.rename("test.cat","input.cat")

os.chdir("..")
k=-11 
out_mag_lst = []   
catalog = open("output.cat",'r')
#Select 5 random sources to test
out_coord = []
# import random
# for i in [random.randint(0,10) for i in range(5)]: 
for line in catalog:
    line = line.split()
    if (line[0]!='#'):
        ra = float(line[2])
        dec = float(line[3])
        mag=float(line[10])#*10**(9)
        print ("[ra,dec]: {}".format([ra,dec]))
        print ("mag_isocorr: {}".format(mag))
        out_coord.append([ra,dec])
        out_mag_lst.append(mag)
out_coord = np.array(out_coord)
out_ra_lst = out_coord[::,0]
out_dec_lst = out_coord[::,1]


os.chdir("r")
for r_band_inputs in all_r_input:
    os.system("sex  {}".format(r_band_inputs))
    os.rename("test.cat","input.cat")
    k=-11 
    mag_lst = []   
    catalog = open("input.cat",'r')
    #Select 5 random sources to test
    coord = []
    # import random
    # for i in [random.randint(0,10) for i in range(5)]: 
    for line in catalog:
        line = line.split()
        if (line[0]!='#'):
            ra = float(line[2])
            dec = float(line[3])
            mag=float(line[10])#*10**(9)
            print ("[ra,dec]: {}".format([ra,dec]))
            print ("mag_isocorr: {}".format(mag))
            coord.append([ra,dec])
            mag_lst.append(mag)
            # break
    import numpy as np
    coord = np.array(coord)
    ra_lst = coord[::,0]
    dec_lst = coord[::,1]
    # plt.plot(ra_lst,dec_lst,'o',color="blue")

# plt.plot(out_ra_lst,out_dec_lst,'*',color="red",markersize=8)
# plt.show()


