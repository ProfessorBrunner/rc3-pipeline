#Change to "sextractor" command on UNIX machines
#Analysis Script: 
# Running SExtractor on 
# Checking Astrometry
# Conduct all our analysis on r band
#crash at '39718'
import numpy as np
from astropy.io import fits
import glob
import os
import shutil
import matplotlib.pyplot as plt
import astropy.io.fits as pf
import montage_wrapper as montage
# PGC = 243
mega_rms=[]
mega_in=[]
NUM_SOURCES=0 #Number Count of sources actually written into the input and output mag
NUM_EDGE_REJECT = 0 #number of sources rejected because it lied too close to the boundary
NUM_RC3_REJECT=0
for PGC in os.walk('.').next()[1][1:]:
    if PGC=="r": 
	continue
    print "PGC: {}".format(PGC)
    for i in glob.glob("default.*"):
        shutil.copy(i,"{}/".format(PGC))
    os.chdir(str(PGC))
    os.chdir("r")
    all_r_input = glob.glob("rawdir/frame-*")
    f=all_r_input[0]
    rc3_data = np.loadtxt("../../rc3_ra_dec_diameter_pgc.txt")
    _dummy =np.where(rc3_data[::,3]==float(PGC))[0][0]
    rc3_ra = rc3_data[::,0][_dummy]
    rc3_dec = rc3_data[::,1][_dummy] #Note these aren't the newly updated ones
    ImageData, ImageHdr = fits.getdata(f, 0, header=True)
    for i in  ['NMGY','NMGYIVAR','EXPTIME','BZERO','BSCALE','SOFTBIAS','BUNIT','FLAVOR','OBSERVER','OBJECT','DRIFT','TIMESYS','RUN','FRAME','CCDLOC','STRIPE','STRIP','ORIGIN','TELESCOP','SCDMETHD','SCDWIDTH','SCDDECMF','SCDOFSET','SCDDYNTH','SCDSTTHL','SCDSTTHR','SCDREDSZ','SCDSKYL','SCDSKYR','COMMENT','VERSIDL','VERSUTIL','VERSPOP','PCALIB','PSKY','RERUN','HISTORY','COMMENT','CAMROW','BADLINES','EQUINOX','FILTER','CAMCOL','VERSION','DERV_VER','ASTR_VER','ASTRO_ID','BIAS_ID','FRAME_ID','KO_VER','PS_ID','ATVSN','FOCUS','DATE-OBS','TAIHMS','SYS_SCN','EQNX_SCN','NODE','INCL','XBORE','YBORE','SYSTEM','CCDMODE','C_OBS','COLBIN','ROWBIN','DAVERS','RADECSYS','SPA','IPA','IPARATE','AZ','ALT','TAI','SPA','IPA','IPARATE','AZ','ALT']:
        try: 
            ImageHdr.remove(i) 
        except(ValueError):
            pass
    fits.writeto(f,ImageData,ImageHdr,clobber=True)
    os.chdir("..")
    k=-11 
    out_mag_lst = []   
   
    # For Boundary source detection
    x = pf.getdata("check.fits")# Don't flip the array for this analysis, we don't need it to be north up
    width = x.shape[0] #all the output mosaics that I have cropped are squares 
    # Load in data  
    catalog = open("output.cat",'r')
    out_coord = []
    for line in catalog:
        line = line.split()
        if (line[0]!='#'):
            ra = float(line[2])
            dec = float(line[3])
            mag=float(line[10])#*10**(9)
	    radius  = float(line[1]) # Estimate: Object are not circular
	    xmin = float(line[4])
            ymin = float(line[5])
            xmax = float(line[6])
            ymax = float(line[7])
            xi = float(line[8])
            yi = float(line[9])
            # Boundary Source Rejection
	    # Cutting away even more boundary sources by increasing size of "radius" margin
 	    radius=radius
            if ((xmin-radius)<=0 ) or ((ymin-radius)<=0) or ((xmax+radius)>=width)or ((ymax+radius)>=width):
                #print ("Source is out of bounds: Source Rejected")
		pass
		#NUM_EDGE_REJECT +=1
            else:
	        out_coord.append([ra,dec])
                out_mag_lst.append(mag)
    out_coord = np.array(out_coord)
    out_ra_lst = out_coord[::,0]
    out_dec_lst = out_coord[::,1]
    
    os.chdir("r")
    for r_band_inputs in all_r_input:
        #os.system("sextractor  {}".format(r_band_inputs))
        #os.rename("test.cat","input.cat")
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
  #      print ("No matched sources for PGC {}".format(PGC))
        #print(os.getcwd())
	os.chdir("../../")
        if os.path.exists("../2000no_matched/{}/".format(PGC)):
             os.system("rm -r {}/".format(PGC))
        else:
             os.system("mv {} ../2000no_matched/".format(PGC))
        continue
    for i in matched_coord[::,0]:
        for j in out_coord_mag:
            if i[0]==j[0]:
#	        print "matched_coord: ",i
 #               print "output_within_region_with_mag:",j
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
 #   print "matched_mag_lst_input: ", matched_mag_lst_input
  #  print "matched_mag_lst_output: ", matched_mag_lst_output 
 #   print "mag_rad_lst:", mag_rad_lst
#
    
    #Matching up radius and magnitude using mag_rad_lst so that we can also store it into the output files
    write_in_input = []
    for  j in matched_mag_lst_input:
	for i in mag_rad_lst:
		if i[0] == j[2]:
#			print "matched!"
			j = list(j)
			# since the mags are only 5 decimal point, there is sometime the weird error where you.
			# have more than one sources with the same mags, which means that the same j would 
			#appeind different corresponding radius values twice, resulting in a list of length 5
			# So this results in an numpy array that is not rectangular (sort of like a gnomon)
			# http://stackoverflow.com/questions/10920318/numpy-beginner-writing-an-array-using-numpy-savetxt			 # This would stil be a valid array but just not a legal 2D array so then this is why
			# numpy.savetxt is not okay with taking this in and writing it in the textfile. 
			if len(j)==3:
				j.append(i[1])
 # 			print "j: ",j 
   			#write_in_input.append(np.array(j,dtype='float64'))
			write_in_input.append(j)
#    print "matched_mag_lst_input:", matched_mag_lst_input
#    print " write_in_input:" , write_in_input
#    print "matched_mag_lst_output:", matched_mag_lst_output
    write_in_input=np.array(write_in_input)
    #print "afterwards:" , write_in_input
   
#    print "size!:" 
#    print len(matched_mag_lst_output)
#    print write_in_input.shape[0]
    #if len(matched_mag_lst_output) ==write_in_input.shape[0]:
    #if len(matched_mag_lst_output) == len(matched_mag_lst_input):
    #    with open("input_mag","a") as in_file:
            # np.savetxt(mag_file,(matched_mag_lst_input,matched_mag_lst_output))
   #    	    np.savetxt(in_file,matched_mag_lst_input)
	    #np.savetxt(in_file,np.array([[1,2],[3,4]]))
    #    with open("output_mag","a") as out_file:
	    # you don't actually need to write this for the output since they are matched, also you can't because no mag_rad_lst written in in the beginning
     #       np.savetxt(out_file,matched_mag_lst_output)
#    os.system("mv {} ../2000finished_post_analysis".format(PGC))  
#    print matched_mag_lst_input
    matched_mag_lst_output=np.array(matched_mag_lst_output)
    matched_mag_lst_input=np.array(matched_mag_lst_input)
 
    #print "NUM_EDGE_REJECT: ",NUM_EDGE_REJECT 
#shutil.move(PGC,"finished_post_analysis/")
    # np.savetxt("input_output_mag",)

# plt.plot(-np.arange(10),-np.arange(10)) #Slope seems to be 1 but off by a constant offset

# plt.show()
    #Doing post processing on this data:
    if (len(matched_mag_lst_output[::,2])==len(matched_mag_lst_input[::,2])):
    	rms = np.sqrt((matched_mag_lst_output[::,2]-matched_mag_lst_input[::,2])**2)
    	#print rms
    	mega_rms.append(rms)
    	mega_in.append(matched_mag_lst_output[::,2])
    	idx = np.where(rms>1.0)[0]
	if (len(idx)!=0):
	    print "outliers rms: {}".format(rms[idx])
	    print "outlier's output mag: {}".format(matched_mag_lst_output[::,2][idx])
	#if (len(idx)!=0):
	#    print "Outlier at count: "
	#    print NUM_SOURCES+idx
	    # Rejecting Boundary Sources (More Stringent Criteria)
	x = pf.getdata("check.fits")# Don't flip the array for this analysis, we don't need it to be north up
    	width = x.shape[0]
        print os.getcwd()
	os.chdir(PGC)
	catalog = open("output.cat",'r')
        mag_of_sources_that_lie_too_close_to_boundary = []
	mag_of_sources_that_lie_too_close_to_RC3=[]
        for line in catalog:
            line = line.split()
            if (line[0]!='#'):
                ra = float(line[2])
                dec = float(line[3])
                mag=float(line[10])#*10**(9)
                radius  = float(line[1]) # Estimate: Object are not circular
                xmin = float(line[4])
                ymin = float(line[5])
                xmax = float(line[6])
                ymax = float(line[7])
                xi = float(line[8])
                yi = float(line[9])
                # Boundary Source Rejection
                # Cutting away even more boundary sources by increasing size of "radius" margin
                radius=4*radius # Object are not circular so they might be cut off on boundary but not registered on the first pass
		# rc3_data = np.loadtxt("../rc3_ra_dec_diameter_pgc.txt")
		# _dummy =np.where(rc3_data[::,3]==float(PGC))[0][0]
		rc3_radius = rc3_data[::,2][_dummy]
		#d2RC3 tells you how far away this source object is from the RC3 galaxy.
		d2RC3 = np.sqrt((rc3_data[::,0][_dummy]-ra)**2+(rc3_data[::,1][_dummy]-dec)**2)
		#print d2RC3
		#print rc3_radius
                if ((xmin-radius)<=0 ) or ((ymin-radius)<=0) or ((xmax+radius)>=width)or ((ymax+radius)>=width):
                    #print ("Source is out of bounds: Source Rejected")
                    #NUM_EDGE_REJECT +=1
                    mag_of_sources_that_lie_too_close_to_boundary.append(mag)
		elif (d2RC3<rc3_radius):
		    mag_of_sources_that_lie_too_close_to_RC3.append(mag)
#		    print ("Source is too close to a RC3, Deblending issue")
        #print "too close: "
	#print mag_of_sources_that_lie_too_close_to_boundary
	print "before: ", len(matched_mag_lst_output)
        for i in matched_mag_lst_output[::,2][idx]:
	    #print "i,j:{},{}".format(i,j) 
            for j in mag_of_sources_that_lie_too_close_to_boundary:
            	#print "i,j:{},{}".format(i,j)
		if i==j:
                    print "Rejected boundary sources on second level!"
		    NUM_EDGE_REJECT=NUM_EDGE_REJECT+1
		    _idx= np.where(matched_mag_lst_output[::,2]==j)[0][0]
		    matched_mag_lst_output =np.delete(matched_mag_lst_output,_idx,0)
		    matched_mag_lst_input =np.delete(matched_mag_lst_input,_idx,0)
	    for k in mag_of_sources_that_lie_too_close_to_RC3:
                #print "i,j:{},{}".format(i,j)
                if i==k:
                    print ("Source is too close to a RC3, Deblending issue")
		    NUM_RC3_REJECT=NUM_RC3_REJECT+1
		    _idx= np.where(matched_mag_lst_output[::,2]==k)[0][0]
                    matched_mag_lst_output =np.delete(matched_mag_lst_output,_idx,0)
                    matched_mag_lst_input =np.delete(matched_mag_lst_input,_idx,0)
	print "after: ", len(matched_mag_lst_output)
	print "after: ", len(matched_mag_lst_input)

        #"Slipping through. Outlier is not boundary sources. Is it a wrongly deblended RC3 galaxy?"
  		
    	#Desired idx for non outlier pairs.
	os.chdir("..")
        if os.path.exists("../2000finished_post_analysis/{}/".format(PGC)):
             os.system("rm -r {}/".format(PGC))
        else:
             os.system("mv {} ../2000finished_post_analysis/".format(PGC))	

	if len(matched_mag_lst_output) == len(matched_mag_lst_input):
	    with open("input_mag","a") as in_file:
                np.savetxt(in_file,matched_mag_lst_input)
            with open("output_mag","a") as out_file:
            	np.savetxt(out_file,matched_mag_lst_output)
	print "NUM_RC3_REJECT: ",NUM_RC3_REJECT
	print "NUM_EDGE_REJECT: ",NUM_EDGE_REJECT
