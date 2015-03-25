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
# PGC = 243
for PGC in os.walk('.').next()[1][1:]:
    print "PGC: {}".format(PGC)
    for i in glob.glob("default.*"):
        shutil.copy(i,"{}/".format(PGC))
    os.chdir(str(PGC))
    os.system("sextractor  SDSS_r_{}r.fits".format(PGC))
    os.rename("test.cat","output.cat") #rename it more appropriately as output catalog
    # with open("output.txt",'r') as f:
    #     for line in f:
    #         print ()
    #-------------------------------------#

    for i in glob.glob("default.*"):
        shutil.copy(i,"{}/".format("r"))
    os.chdir("r")
    all_r_input = glob.glob("raw/frame-*")
    os.system("sextractor  {}".format(all_r_input[0]))
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
        os.system("sextractor  {}".format(r_band_inputs))
        os.rename("test.cat","input.cat")
        k=-11
	mag_rad_lst = [] 
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
		radius = float(line[1])
                # print ("[ra,dec]: {}".format([ra,dec]))
                # print ("mag_isocorr: {}".format(mag))
                coord.append([ra,dec])
                mag_lst.append(mag)
		mag_rad_lst.append([mag,radius])
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
    idx_ra =np.intersect1d(np.where(min(out_ra_lst)<coord[::,0]+epsilon)[0],np.where(coord[::,0]<max(out_ra_lst)+epsilon)[0])
    idx_dec = np.intersect1d(np.where(min(out_dec_lst)<coord[::,1]+epsilon)[0],np.where(coord[::,1]<max(out_dec_lst)+epsilon)[0])
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
        print(os.getcwd())
	os.chdir("../../")
	os.system("mv {} ../500no_matched/".format(PGC))
        continue
    for i in matched_coord[::,0]:
        for j in out_coord_mag:
            if i[0]==j[0]:
	        print "matched_coord: ",i
                print "output_within_region_with_mag:",j
                matched_mag_lst_output.append(j)
    # Matching coordinates with input magnitudes
    matched_mag_lst_input =[]
    for i in matched_coord[::,1]:
        for j in input_within_region_with_mag:
            if i[0]==j[0]:
#		print "matched_coord: ",i
#		print "input_within_region_with_mag:",j
                matched_mag_lst_input.append(j)
    #plt.plot(matched_mag_lst_output,matched_mag_lst_input,'o')
    os.chdir("../..")
    print "matched_mag_lst_input: ", matched_mag_lst_input
    print "matched_mag_lst_output: ", matched_mag_lst_output 
    print "mag_rad_lst:", mag_rad_lst

    
    #Matching up radius and magnitude using mag_rad_lst so that we can also store it into the output files
    write_in_input = []
    for  j in matched_mag_lst_input:
	for i in mag_rad_lst:
		if i[0] == j[2]:
			print "matched!"
			j = list(j)
			# since the mags are only 5 decimal point, there is sometime the weird error where you.
			# have more than one sources with the same mags, which means that the same j would 
			#appeind different corresponding radius values twice, resulting in a list of length 5
			# So this results in an numpy array that is not rectangular (sort of like a gnomon)
			# http://stackoverflow.com/questions/10920318/numpy-beginner-writing-an-array-using-numpy-savetxt			 # This would stil be a valid array but just not a legal 2D array so then this is why
			# numpy.savetxt is not okay with taking this in and writing it in the textfile. 
			if len(j)==3:
				j.append(i[1])
  			print "j: ",j 
   			#write_in_input.append(np.array(j,dtype='float64'))
			write_in_input.append(j)
#    print "afterwards:", matched_mag_lst_input
#    print "afterwards:" , write_in_input
    print "matched_mag_lst_output:", matched_mag_lst_output
    write_in_input=np.array(write_in_input)
    print "afterwards:" , write_in_input
   
    print "size!:" 
    print len(matched_mag_lst_output)
    print write_in_input.shape[0]
    if len(matched_mag_lst_output) ==write_in_input.shape[0]:
        with open("input_mag","a") as in_file:
            # np.savetxt(mag_file,(matched_mag_lst_input,matched_mag_lst_output))
       	    np.savetxt(in_file,write_in_input)
	    #np.savetxt(in_file,np.array([[1,2],[3,4]]))
        with open("output_mag","a") as out_file:
	    # you don't actually need to write this for the output since they are matched, also you can't because no mag_rad_lst written in in the beginning
            np.savetxt(out_file,matched_mag_lst_output)
    os.system("mv {} ../500finished_post_analysis".format(PGC))    
#shutil.move(PGC,"finished_post_analysis/")
    # np.savetxt("input_output_mag",)

# plt.plot(-np.arange(10),-np.arange(10)) #Slope seems to be 1 but off by a constant offset

# plt.show()
