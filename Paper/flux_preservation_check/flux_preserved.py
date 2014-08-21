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
		if (n<100):
			a = str(line)[0]
	        # Useful for debugging purpose, put this in the rc3_ra_dec_pgc.txt to start from where you left off (when error)
			if a[0] =="@": 
				start=True
				continue
			if (start):
				n +=1
				ra = float(line.split()[0])
				dec = float(line.split()[1])
				radius = float(line.split()[2])/2. #radius = diameter/2
				pgc=str(line.split()[3]).replace(' ', '')
				clean=True
				rc3Obj= RC3(ra,dec,radius,pgc)
	# #pgc58 = RC3(0.184583333333,28.4013888889,0.0132388039385,58)
	# rc3Obj = RC3(5.5,22.4002777778,0.01177114622875,1412)
	#getting the raw data from SkyServer
	 #def getData(self,band,run, camcol,field,rerun=301):
				ss = SkyServer()
				info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
				print info
				r_mosaic = ""
				for i in info:
					r_mosaic=ss.getData('r',i[0],i[1],i[2])
				#Data after mosaicing
				rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
				rc3Obj.source_info(rfits,SDSS())
				import os
				#r_mosaic = "1412/SDSS_r_1412.fits"
				os.system("sextractor  {}".format(r_mosaic))
				#Trying this on original data first to see if it matches what's inside FITS header
				# os.system("sex frame-r-007917-3-0139.fits")
				catalog = open("test.cat",'r')
				mag_lst = []    	
				for line in catalog:
					line = line.split()
					if (line[0]!='#'):
				    	#MAG_ISOCOR      Corrected isophotal magnitude                   [mag]
				    	# in MGY conver to NMGY
						mag=float(line[10])*10**(9)
						mag_lst.append(mag)
				#print mag_lst
				mag_rawdata.append(sum(mag_lst))

				print ("r_mosaic: {}".format(r_mosaic))
				#os.system("sextractor {}".format(r_mosaic))
				import glob
				x= glob.glob("frame-*")
				print (x)
				print (x[0])
				os.system("sextractor {}".format(x[0]))
				catalog = open("test.cat",'r')
				mag_lst = []    	
				for line in catalog:
				    line = line.split()
				    if (line[0]!='#'):
				    	#MAG_ISOCOR      Corrected isophotal magnitude                   [mag]
				    	# in MGY conver to NMGY
				        mag=float(line[10])*10**(9)
				        mag_lst.append(mag)
				mag_mosaic.append(sum(mag_lst))
		os.system("rm frame-*")
		print (mag_mosaic)
		print (mag_rawdata)
	print (mag_mosaic)
	print (mag_rawdata)
