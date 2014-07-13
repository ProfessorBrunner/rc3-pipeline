# Class for interacting with SDSS's SkyServer
from  server import Server
import sqlcl
import abc 
import os
class SkyServer(Server):
	#Default constructor
    def __init__ (self):
    	# print("SkyServer constructor")
    	super(SkyServer,self).__init__()
        self.name = 'SkyServer'

	
    def query(self,query):
		# other_rc3s = sqlcl.query("SELECT distinct rc3.pgc,rc3.ra,rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{1} and  {0}+{1} and po.dec between {2}-{3} and  {2}+{3}".format(str(rc3_ra),str(margin),str(rc3_dec),str(margin))).readlines()
        result = sqlcl.query(query).readlines()
        data =[]
        count =0
        for i in result:
            if count>1:
                list =i.split(',')
                list[2]= list[2][:-1]
                data.append(list)
            count += 1 
        #print (result)
        return (data)

    def getData(self,band,run, camcol,field,rerun=301):	
        out = "frame-{}-{}-{}-{}".format(band,str(run).zfill(6),str(camcol),str(field).zfill(4))
        os.system("wget http://mirror.sdss3.org/sas/dr10/boss/photoObj/frames/301/{}/{}/{}.fits.bz2".format(str(run),str(camcol),out) )
        os.system("bunzip2 {}.fits.bz2".format(out))

    #########################
    #    Query Builder		#
    #########################
    def other_rc3():
    	'''
    	return a list of other rc3 that lies in the same field
    	'''

        


    # def test():
    # 	print ("test")
    # def str(self):
    #    super.str(self)