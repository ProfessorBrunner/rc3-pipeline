#Change to "sextractor" command on UNIX machines
#Analysis Script: 
# Running SExtractor on 
# Checking Astrometry
# Conduct all our analysis on r band
#crash at '39718'
import numpy as np
import glob
import os
import shutil
import matplotlib.pyplot as plt
for PGC in os.walk('.').next()[1][1:]:
    print PGC
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
            # print ("[ra,dec]: {}".format([ra,dec]))
            # print ("mag_isocorr: {}".format(mag))
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
                # print ("[ra,dec]: {}".format([ra,dec]))
                # print ("mag_isocorr: {}".format(mag))
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

    mag_lst = np.array(mag_lst)
    idx = np.where(abs(mag_lst-out_mag_lst[0])<0.1)
    epsilon = 0.001#small margin
    idx_ra = np.intersect1d(np.where(min(out_ra_lst)<coord[::,0]+epsilon),np.where(coord[::,0]<max(out_ra_lst)+epsilon))
    idx_dec = np.intersect1d(np.where(min(out_dec_lst)<coord[::,1]+epsilon),np.where(coord[::,1]<max(out_dec_lst)+epsilon))
    intersect = np.intersect1d(idx_ra,idx_dec)
    input_within_region  = coord[intersect]
    input_within_region_with_mag =np.c_[input_within_region, mag_lst[intersect]] 
    # plt.plot(input_within_region[::,0],input_within_region[::,1],'o')
    # plt.plot(out_ra_lst,out_dec_lst,'o',color="red",ms=5)
    # plt.show()
    matched_coord = []
    for i in out_coord:
        for o in input_within_region:
            bool = (abs(i-o)<5e-4)
            if(bool[0] and bool[1]):
                matched_coord.append([i,o])
    out_coord_mag = np.c_[out_coord, out_mag_lst] 
    # Matching coordinates with output magnitudes
    matched_coord=np.array(matched_coord)
    matched_mag_lst_output =[]
    if len(matched_coord)==0:
        print ("No matched sources for PGC {}".format(PGC))
        os.getcwd()
        os.chdir("../../")
        continue
    for i in matched_coord[::,0]:
        for j in out_coord_mag:
            if i[0]==j[0]:
                matched_mag_lst_output.append(j[2])
    # Matching coordinates with input magnitudes
    matched_mag_lst_input =[]

    for i in matched_coord[::,1]:
        for j in input_within_region_with_mag:
            if i[0]==j[0]:
                matched_mag_lst_input.append(j[2])
    plt.plot(matched_mag_lst_output,matched_mag_lst_input,'o')
    os.chdir("../..")
    with open("input_mag","a") as in_file:
        # np.savetxt(mag_file,(matched_mag_lst_input,matched_mag_lst_output))
        np.savetxt(in_file,matched_mag_lst_input)
    with open("output_mag","a") as out_file:
        np.savetxt(out_file,matched_mag_lst_output)
    # np.savetxt("input_output_mag",)

# plt.plot(-np.arange(10),-np.arange(10)) #Slope seems to be 1 but off by a constant offset

# plt.show()
