# Class for interacting with SDSS's SkyServer
from  server import Server
import sqlcl
import abc 
import os
import time
DEBUG = False
class SkyServer(Server):
	#Default constructor
    def __init__ (self):
    	if (DEBUG):print("SkyServer constructor")
    	super(SkyServer,self).__init__()
        self.name = 'SkyServer'

    def query(self,query):
        result = sqlcl.query(query).readlines()
        data =[]
        count =0
        if (DEBUG): print (result)
        for i in result:
            if count>1:
                list =i.split(',')
                if (len(list)>2):
                    list[2]= list[2][:-1]
                    data.append(list)
            count += 1 
        if (DEBUG):print (result)
        if (len(data)>0):
            if (len(data[0])>0):
                while (data[0][0][1:6]=="ERROR"):
                    #Case where doing more than 60 queries in 1 minute
                    print("ERROR: Too much query in 1 minute. Sleep for 60 second.")
                    time.sleep(60)
                    data = self.query(query)
        return (data)

    def getData(self,band,run, camcol,field,rerun=301):	
        out = "frame-{}-{}-{}-{}".format(band,str(run).zfill(6),str(camcol),str(field).zfill(4))
        os.system("wget http://mirror.sdss3.org/sas/dr10/boss/photoObj/frames/301/{}/{}/{}.fits.bz2".format(str(run),str(camcol),out) )
        os.system("bunzip2 {}.fits.bz2".format(out))

 
    #########################
    #    Query Builder		#
    #########################
    # Overriding otherRC3 in Server class
    def otherRC3(self,ra,dec,margin):#,survey):
        
    	'''
    	Given ra,dec, pgc of an RC3 galaxy, return a list of other rc3 that lies in the same margin field.
        >>> from sdss import SDSS
        >>> from skyserver import SkyServer
        >>> s = SkyServer()
        >>> s.otherRC3(0.0891,-2.6105,1,SDSS())
        [['PGC    23', '0.089583', '-2.612056'], ['PGC   205', '0.773583', '-1.913806']]
    	'''
        query = "SELECT distinct rc3.pgc,rc3.ra,rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{2} and  {0}+{2} and po.dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
        return self.query(query)
        
    def surveyFieldConverter(self,ra,dec,margin,need_clean=False):
    	'''
    	Given ra,dec ,return a list of run camcol field for the given ra,dec
    	'''
        if (need_clean):
            query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
        else:
            query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
        return self.query(query)

