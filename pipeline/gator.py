# Class for interacting with IPAC's  Gator API 
from  server import Server
import abc
import re
import os
class Gator(Server):
    '''
    Possible surveys: 2MASS, WISE, IRAS
    '''
    def __init__(self):

        self.name = 'Gator'
    
    def query (self,query,survey,catalog='default'): 
        '''
        Query the server database
        URL query form : http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?parameter1=value1&parameter2=value2&
        '''
        print ("querying: "+"wget {}http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?{}{}".format(' "',query,'" '))
        os.system("wget -O result.txt {}http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?{}{}".format(' "',query,'" '))
        # Parse results into a list 
    def getData(self,band,ra,dec,margin,survey):	
        '''
        Downloads imaging data from server
        URL query form : http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-im_sia?
        
        FORMAT image/fits
		Return URIs for image FITS files

		POS=ra,dec &SIZE = margin
        '''


        # print ("getData")
        out = "FORMAT=image/fits&band={}&POS={},{}&SIZE={}".format(band,str(ra),str(dec),str(margin))
        os.system("wget -O tbl.xml {}http://irsa.ipac.caltech.edu/cgi-bin/{}/IM/nph-im_sia?{}{}".format(' "',survey.name,out,'" '))
        print ("wget -O tbl.xml {}http://irsa.ipac.caltech.edu/cgi-bin/{}/IM/nph-im_sia?{}{}".format(' "',survey.name,out,'" '))
        #Parse XML to find URL of all objects lying inside field 
        with open("tbl.xml") as f:
            print ("here")
            n=0
            i=0
            for line in f:
                # print line
                #The URL is stored in the line two lines after <TR>
                # print line[:4]
                if (line[:4] =="<TR>" or n==1):
                    #passing till 2 lines down <TR>
                    n+=1
                    pass
                elif (n==2):
                    n=0
                    url = line.split('[')[-1].split(']')[0]
                    # print(url)
                    if (i>0):
                        #preventing other downloads to override the initial file
                        filename = "{}_{}_{}_{}_{}.fits".format(survey.name,band,str(ra),str(dec),str(i))
                    else:
                        filename = "{}_{}_{}_{}.fits".format(survey.name,band,str(ra),str(dec))
                    print ("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    os.system("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    i+=1


    #########################
    #    Query Builder		#
    #########################
    def otherRC3(self,ra,dec,margin,survey,catalog='default'): 
        '''
        Given ra,dec, pgc of an RC3 galaxy, return a list of other rc3 that lies in the same margin field.
        Units
        =====
        Search radius (radius): arcsecond
        Search box (size): arcsecond
        '''
        if (survey.name=='2MASS'):
            catalog = 'fp_xsc' #Default as extended source catalog
        elif(survey.name=='WISE'):
            #prob 3 Cryo ?
            pass
        ##############
        #NOTE THIS DOESN'T ACTUALLY FIND ANY OTHER RC3 GALAXY, IT JUST SEARCHES FOR THE TILES INSIDE THE BOX
        #degree to arcsecond conversion 
        margin = margin*3600
        query = "spatial=box&catalog={}&size={}&outfmt=1&objstr={},{}".format(catalog,str(margin),str(ra),str(dec))
        print(query)
        return self.query(query,survey,catalog)
        # TILES converter is not necessary because we can just get the image from getData
    # def runCamcolFieldConverter(self,ra,dec,margin,need_clean=False):
    #     '''
    #     Given ra,dec ,return a list of run camcol field for the given ra,dec
    #     '''
    #     if (need_clean):
    #         query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
    #     else:
    #         query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
    #     return self.query(query)