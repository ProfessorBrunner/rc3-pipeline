# Class for interacting with IPAC's  Gator API 
from astropy import *
from astroquery.vizier import *
from astroquery.irsa import Irsa
import astropy.units as u
from astropy import coordinates
from astropy.coordinates import FK5
#from astropy.coordinates import SkyCoord
from  server import Server
import abc
import re
import os
#Supressing warnings due to version differences in astroquery and astropy (dev 0.4)
import warnings
DEBUG = False
warnings.filterwarnings('ignore',message='profile')
warnings.filterwarnings('ignore',message='_astropy_init')
warnings.filterwarnings('ignore',message='ConfigurationDefaultMissingWarning ')
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

        out = "FORMAT=image/fits&band={}&POS={},{}&SIZE={}".format(band,str(ra),str(dec),str(margin))
        os.system("wget -O tbl.xml {}http://irsa.ipac.caltech.edu/cgi-bin/{}/IM/nph-im_sia?{}{}".format(' "',survey.name,out,'" '))
        if (DEBUG):print ("wget -O tbl.xml {}http://irsa.ipac.caltech.edu/cgi-bin/{}/IM/nph-im_sia?{}{}".format(' "',survey.name,out,'" '))
        #Parse XML to find URL of all objects lying inside field 
        with open("tbl.xml") as f:
            n=0
            i=0
            for line in f:
                if (line[:4] =="<TR>" or n==1):
                    #passing till 2 lines down <TR>
                    n+=1
                    pass
                elif (n==2):
                    n=0
                    url = line.split('[')[-1].split(']')[0]
                    if (i>0):
                        #preventing other downloads to override the initial file
                        filename = "{}_{}_{}_{}_{}.fits".format(survey.name,band,str(ra),str(dec),str(i))
                    else:
                        filename = "{}_{}_{}_{}.fits".format(survey.name,band,str(ra),str(dec))
                    if (DEBUG) : print ("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    os.system("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
                    i+=1


    #########################
    #    Query Builder		#
    #########################
    #Should just inherit otherRC3 from Server
    def surveyFieldConverter(self,ra,dec,margin,need_clean=False,cat = 'fp_xsc'):
        '''
        for 2MASS return the designation for each detected source in search field 
        '''
        pos = FK5(ra*u.degree, dec*u.degree)
    	#pos = coordinates.SkyFrame(ra*u.deg,dec*u,deg, frame='fk5')
        #pos =SkyCoord(ra* u.deg,dec* u.deg, frame='fk5')
        tbl = Irsa.query_region(pos,catalog=cat, spatial='Box',width=2*margin*u.deg)
        lst=[]
        if (need_clean and len(tbl)>0):
            for i in range(len(tbl['designation'])):
                if (tbl[0]['cc_flg']=='0'):
                    lst.append(tbl[i]['designation'])
            return lst
        else:
            return list(tbl['designation'])
