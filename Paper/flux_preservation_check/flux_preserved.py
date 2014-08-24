from sdss import SDSS
from rc3 import *
from skyserver import *
with open("sample.txt",'r') as f:
    mag_mosaic=[]
    mag_rawdata = []
    allObj=[]
    n = 0
    start=False
    for line in f:
        a = str(line)[0]
        if a[0] =="@": 
            start=True
            continue
        if (start):
            n +=1
            ra = float(line.split()[0])
            dec = float(line.split()[1])
            new_ra = float(line.split()[2])
            new_dec = float(line.split()[3])
            radius = float(line.split()[4])
            pgc=str(line.split()[5]).replace(' ', '')
            clean=True
            rc3Obj= RC3(ra,dec,radius,pgc)
            ss = SkyServer()
            info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
            for i in info:
                ss.getData('r',i[0],i[1],i[2])
            import glob
            # Selecting any one raw data field, no need to sum together the flux from all fields
            x= glob.glob("frame-*")
            print (x)
            print ("There are {} fields in this region".format(len(x)))
            if (len(x)==1):
		print "only one field in region"
		continue
	    print (x[0])
            import os
            os.system("sextractor  {}".format(x[0]))
            # Find total flux in image of one field in the raw data 
            catalog = open("test.cat",'r')
            mag_lst = []    
            # n=0   
            # for line in catalog:
            #   line = line.split()
            #   print (line)
            #   #print ("line1: {}".format(line[2]))
            #   #print ("line2: {}".format(line[3]))
            #   #print ("new_ra: {}".format(new_ra))
            #   #print ("new_dec: {}".format(new_dec))
            #   if (line[0]!='#' and n==0):
            #       # selected in sample.txt no source confusion jsut largest source compare flux
            #    #and line[2]==new_ra and line[3]==new_dec):
            #   #   n=n+1
            #       #Verfiy that this is the source of interetest (already previously updated)
            #       #We only obtain flux value for individual objects
            #       #MAG_ISOCOR      Corrected isophotal magnitude                   [mag]
            #       # in MGY conver to NMGY
            #       mag=float(line[10])#*10**(9)
            #       print "mag: {} ".format(mag)
            #       mag_lst.append(mag)
            #       break
            #Conduct pairwise comparison
            catalog = open("test.cat",'r')
            #Creating a list of radius
            radius_list = []    
	    # Creating a corresponding list of ra,dec
            sextract_dict ={}
            for line in catalog:
                line = line.split()
                if (line[0]!='#'):
                    radius=np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2
                    radius_list.append(radius)
                    coord = np.array([float(line[2]),float(line[3])])
                    sextract_dict[radius]=coord
            if (DEBUG): print ("Radius: "+str(radius_list))
            print ("Source is Obvious")
            n=1 # Just keep the maximum radius
            #Creating a list of radius
            catalog = open("test.cat",'r')
            radius = []
            for line in catalog:
                line = line.split()
                if (line[0]!='#'):
                    radius.append(np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2)
            if (DEBUG):print (radius)
            #special value reversed for empty list (no object detected by SExtractor)
            catalog = open("test.cat",'r')
            for i in catalog:
                if(DEBUG) :print ("i : {}".format(i))
                line = i.split()
                if (DEBUG): ("line: {}".format(line))
                if (line[0]!='#' ):
                    #Pythagorean method
                    radii = np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2
                    if (radii==max(radius)):
                        print ('Biggest Galaxy with radius {} pixels!'.format(str(radii)))
                        mag=float(line[10])#*10**(9)
                        print "mag: {} ".format(mag)
                        mag_lst.append(mag)
                        break

            print (" mag_lst: "+str(mag_lst))
            mag_rawdata.append(sum(mag_lst))
            os.system("rm test.cat") #ensure no flow through
            #Data after mosaicing
            rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
            rc3Obj.source_info(rfits,SDSS()) #Generate data product
            #Find total flux in mosaiced image
            os.system("cp {0}/SDSS_r_{0}.fits .".format(rc3Obj.pgc))
            os.system("sextractor SDSS_r_{0}.fits".format(rc3Obj.pgc)) #run sextractor in the outer directory where the defaul.* files are stored
            catalog = open("test.cat",'r')
            mag_lst_r = []      
            for line in catalog:
                line = line.split()
                if (line[0]!='#'):
                    mag_r=float(line[10])#*10**(9)
                    mag_lst_r.append(mag_r)
            mag_mosaic.append(sum(mag_lst_r))
        # remove all the data from so that glob doesn't detect previous data files in the next run
        os.system("rm frame-*")
        print ("mag_mosaic= {}".format(mag_mosaic))
        print ("mag_rawdata= {}".format(mag_rawdata))
    print ("mag_mosaic= {}".format(mag_mosaic))
    print ("mag_rawdata= {}".format(mag_rawdata))
