from  server import Server
from twoMass import TwoMass
from gator import Gator
import abc
import re
import os
class DSSServer(Server):
    '''
    A custom server class for DSSServer
    Because of the diverse data source of DSS, this is an agglormerate of things that works on DSS.
    '''

    def __init__(self):
        self.name = 'DSSServer'
    
    def query (self,query): 
        '''
        Query the server database
        URL query form : http://irsa.ipac.caltech.edu/applications/FinderChart/docs/finderProgramInterface.html
        '''
        # print ("querying: "+"wget {}http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?{}{}".format(' "',query,'" '))
        
        os.system("wget -O result.txt {}http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder?{}{}".format(' "',query,'" '))

    def getData(self,band,ra,dec,margin,survey="DSS"):	
        '''
        Downloads imaging data from server
        URL query form : http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-im_sia?
        
        FORMAT image/fits
		Return URIs for image FITS files

		POS=ra,dec &SIZE = margin
        '''
 		# Margin value conversion degree to arcminute 1 degree = 60 arcminutes
 		# Can not specify band?
        q = "locstr={}+{}&survey=dss&mode=prog&subsetsize={}".format(ra,dec,60*margin)
        self.query(q)

        #Parse XML to find URL of all objects lying inside field 
        with open("result.txt") as f:
            n=0
            i=0
            for line in f:
                # The URL is stored in the line  after <fitsurl>
                if (line.strip() =="<fitsurl>"): #or n==0):
                    # print ("n: "+str(n))
                    # print ("i: "+str(i))
                    # passing till 1 lines down <fitsurl>
                    n+=1
                    pass
                elif (n==1):
                    # n=0
                    # print ("here")
                    url = line.split('[')[-1].split(']')[0].strip()
                    print (url)
                    if (i>0):
                        #preventing other downloads to override the initial file
                        filename = "{}_{}_{}_{}_{}.fits".format(survey,band,str(ra),str(dec),str(i))
                    else:
                        filename = "{}_{}_{}_{}.fits".format(survey,band,str(ra),str(dec))
                    print ("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    os.system("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    i+=1


    #########################
    #    Query Builder		#
    ######################### 
    def surveyFieldConverter(self,ra,dec,margin,need_clean=False,cat = 'fp_xsc'):
        '''
        for 2MASS return the designation for each detected source in search field 
        '''
        # pos =SkyCoord(ra* u.deg,dec* u.deg, frame='fk5')
        # tbl = Irsa.query_region(pos,catalog=cat, spatial='Box',width=2*margin*u.deg)
        # lst=[]
        # if (need_clean and len(tbl)>0):
        #     for i in range(len(tbl['designation'])):
        #         if (tbl[0]['cc_flg']=='0'):
        #             lst.append(tbl[i]['designation'])
        #     return lst
        # else:
        #     return list(tbl['designation'])

        