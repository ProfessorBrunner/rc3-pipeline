from rc3 import *
from dssServer import *
from dss import DSS
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
            print (line.split())
            ra = float(line.split()[0])
            dec = float(line.split()[1])
            new_ra = float(line.split()[2])
            new_dec = float(line.split()[3])
            radius = float(line.split()[4])
            pgc=str(line.split()[5]).replace(' ', '')
            clean=True
            rc3Obj= RC3(ra,dec,radius,pgc)
            ss = DSSServer()
            info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
            for i in info:
                ss.getData('r',i[0],i[1],i[2])
            import glob
            # Selecting any one raw data field, no need to sum together the flux from all fields
            x= glob.glob("frame-*")
            print (x)
            print ("There are {} fields in this region".format(len(x)))
            # if (len(x)==1):
            #     print "only one field in region"
            # else:    
            #     print (x[0])
            # import os
            # # os.system("sextractor  {}".format(x[0]))
            # os.system("sex {}".format(x[0]))
            # k=-11 
            # mag_lst = []   
            # catalog = open("test.cat",'r')
            # os.system("rm test.cat") #ensure no flow through
            #Data after mosaicing
            rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,DSS())
            rc3Obj.source_info(rfits,DSS()) #Generate data product
            os.system("rm frame-*")