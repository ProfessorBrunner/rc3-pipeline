#On bigdog point PATH to montage by `` export PATH=${PATH}:/data/small/des/montage/montage/Montage_v3.3/Montage/  ``
from sdss import SDSS
from rc3 import *
from skyserver import *
with open("rc3_subsample.txt",'r') as f:
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
            print (line.split())
            ra = float(line.split()[0])
            dec = float(line.split()[1]) 
            radius = float(line.split()[2])
            # pgc=str(line.split()[3]).replace(' ', '')
            pgc = str(int(float(line.split()[3])))
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
            if (len(x)==0):
                print "Does not lie in SDSS footprint"
                # os.system("rm -r r/")
                continue
            elif (len(x)==1):#we only want to test fields that require mosaicking.
                print "only one field in region "
                # os.system("rm -r r/")
                continue
            else:    
                # print (x[0])
                import os
                #Data after mosaicing
                rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
                rc3Obj.source_info(rfits,SDSS()) #Generate data product
            os.system("rm frame-*")
   #      print ("mag_mosaic= {}".format(mag_mosaic))
   #      print ("mag_rawdata= {}".format(mag_rawdata))
   #  print ("mag_mosaic= {}".format(mag_mosaic))
   #  print ("mag_rawdata= {}".format(mag_rawdata))

