from sdss import SDSS
from rc3 import *
from skyserver import *
#pgc58 = RC3(0.184583333333,28.4013888889,0.0132388039385,58)
rc3Obj = RC3(5.5,22.4002777778,0.01177114622875,1412)
#getting the raw data from SkyServer
 #def getData(self,band,run, camcol,field,rerun=301):
ss = SkyServer()
info = ss.surveyFieldConverter(rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius)
print info
for i in info:
	ss.getData('r',i[0],i[1],i[2])
#Data after mosaicing
rfits =rc3Obj.mosaic_band('r',rc3Obj.rc3_ra,rc3Obj.rc3_dec,3*rc3Obj.rc3_radius,rc3Obj.rc3_radius,rc3Obj.pgc,SDSS())
rc3Obj.source_info(rfits,SDSS())
