
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
			print (x[0])
			import os
			os.system("sextractor  {}".format(x[0]))
			# Find total flux in image of one field in the raw data 
			catalog = open("test.cat",'r')
			print ("here")
			mag_lst = []    	
			for line in catalog:
				line = line.split()
				print ("line1: {}".format(line[2]))
				print ("line2: {}".format(line[3]))
				print ("new_ra: {}".format(new_ra))
				print ("new_dec: {}".format(new_dec))
				n=0
				if (line[0]!='#' and n==0):
					# selected in sample.txt no source confusion jsut largest source compare flux
				 #and line[2]==new_ra and line[3]==new_dec):
					n=n+1
					#Verfiy that this is the source of interetest (already previously updated)
					#We only obtain flux value for individual objects
			    	#MAG_ISOCOR      Corrected isophotal magnitude                   [mag]
			    	# in MGY conver to NMGY
					mag=float(line[10])#*10**(9)
					print "mag: ".format(mag)
					mag_lst.append(mag)

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
		print (mag_mosaic)
		print (mag_rawdata)
	print (mag_mosaic)
	print (mag_rawdata)

