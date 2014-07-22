# Class for interacting with IPAC's  Gator API 
from astropy import *
from astroquery.vizier import *
from astroquery.irsa import Irsa
import astropy.units as u
from astropy.coordinates import SkyCoord
#####################
from  server import Server
import abc
import re
import os
#####################
#Supressing warnings due to version differences in astroquery and astropy (dev 0.4)
import warnings
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
                # print line
                if (line[:4] =="<TR>" or n==1):
                    #passing till 2 lines down <TR>
                    n+=1
                    # print ("pass")
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
    def otherRC3(self,ra,dec,margin,survey): 
        '''
        Given ra,dec, pgc of an RC3 galaxy, return a list of other rc3 that lies in the same margin field.
        in the form including the original galaxy of interest

        [['PGC54', '0.158083', '28.384556'], ['PGC58', '0.183333', '28.401444']]

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
        #query = "spatial=box&catalog={}&size={}&outfmt=1&objstr={},{}".format(catalog,str(margin),str(ra),str(dec))
        rc3Cat = Vizier(catalog='VII/155/rc3')
        pos =SkyCoord(ra* u.deg,dec* u.deg, frame='fk5')
        print(pos)
        rc3_matches=rc3Cat.query_region(pos, radius=2*margin*u.deg)
        print (rc3_matches[0])
        other_rc3s=[]
        if (len(rc3_matches)!=0):
            # It is practically impossible for len to beb zero because the galaxy of interest would always detect itself
            # unless we are using it as a rc3 finder for any ra,dec
            print (len(rc3_matches[0]['PGC']))
            for i in range(len(rc3_matches[0]['PGC'])):
                lst = []
                # print (rc3_matches[0]['PGC'].data)
                lst.append(rc3_matches[0]['PGC'].data[i])
                lst.append(rc3_matches[0]['_RAJ2000'].data[i])
                lst.append(rc3_matches[0]['_DEJ2000'].data[i])
                other_rc3s.append(lst)
        return other_rc3s
        # TILES converter is not necessary because we can just get the image from getData
    def surveyFieldConverter(self,ra,dec,margin,need_clean=False,cat = 'fp_xsc'):
        '''
        for 2MASS return the designation for each detected source in search field 
        '''
        pos =SkyCoord(ra* u.deg,dec* u.deg, frame='fk5')
        tbl = Irsa.query_region(pos,catalog=cat, spatial='Box',width=2*margin*u.deg)
        # print (tbl)
        # print(list(tbl['designation']))
        return list(tbl['designation'])
        
        #This is actually not necessary because the SExtract_dict and radius is returned by SExtractor value  mpt frp, querying results/
    # def otherRC3info(self,ra,dec,margin,survey,catalog='default'):
    #     '''
    #     Given ra,dec, pgc of an RC3 galaxy, return a dict of other rc3 that lies in the same margin field
    #     with keys of radius and value as a list of position ra,dec
    #     in the form 

    #     {58: [0.18333, 28.40144], 54: [0.15808, 28.38455]}

    #     '''
        
    #     #Converting Table results to dictionary form
    #     try :
    #         dict = {}
    #         for i in range(50): 
    #             dict[int(tbl[i]['PGC'][3:])]=(tbl[i]['_RAJ2000'],tbl[i]['_DEJ2000'])
    #             #print (tbl[i])
    #     except(IndexError):
    #         #Intentionally Crash
    #         pass
    #     return dict
    # def runCamcolFieldConverter(self,ra,dec,margin,need_clean=False):
    #     '''
    #     Given ra,dec ,return a list of run camcol field for the given ra,dec
    #     '''
    #     if (need_clean):
    #         query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
    #     else:
    #         query = "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{2} and  {0}+{2}and dec between {1}-{2} and  {1}+{2}".format(str(ra),str(dec),str(margin))
    #     return self.query(query)