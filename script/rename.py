# Script for renaming all the data poduct (FITS and TIFF) 
import glob
import os
# print  [f for f in os.listdir('.') if os.path.isfile(f)]
for i in os.walk('.').next()[1]:
    print ("Working on PGC {} ".format(i))
    os.chdir("{}/sdss".format(i))
    #directory name is pgc number
    try:
        os.rename(glob.glob("SDSS_*_*_BEST.tiff")[0], "SDSS_{}_BEST.tiff".format(i)) 
        os.rename(glob.glob("SDSS_*_*_LOW.tiff")[0], "SDSS_{}_LOW.tiff".format(i)) 
    except(IndexError):
        print("STIFF error")
    try:
        os.rename(glob.glob("SDSS_u_*_*.fits")[0], "SDSS_u_{}.fits".format(i)) 
    except(IndexError):
        print("Missing fits error")
    try:
        os.rename(glob.glob("SDSS_g_*_*.fits")[0], "SDSS_g_{}.fits".format(i)) 
    except(IndexError):
        print("Missing fits error")
    try:
        os.rename(glob.glob("SDSS_r_*_*.fits")[0], "SDSS_r_{}.fits".format(i)) 
    except(IndexError):
        print("Missing fits error")
    try:
        os.rename(glob.glob("SDSS_i_*_*.fits")[0], "SDSS_i_{}.fits".format(i)) 
    except(IndexError):
        print("Missing fits error")
    try:
        os.rename(glob.glob("SDSS_z_*_*.fits")[0], "SDSS_z_{}.fits".format(i)) 
    except(IndexError):
        print("Missing fits error")
    os.chdir("../..")

    # for j in [f for f in os.listdir('.') if os.path.isfile(f)]:

