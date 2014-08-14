'''
The Server object is an abstract class for accessing raw data from survey and feeds it into program in the appropraite format.
'''

import astropy.units as u
from astroquery.vizier import *
#from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
from astropy import coordinates
from abc import ABCMeta , abstractmethod

class Server(object):
    __metaclass__= ABCMeta

    def __init__(self):
        self.name = 'Server'
    
    @abstractmethod
    def query (self,query): 
        '''
        Query the server database
        '''
        raise NotImplementedError()

    @abstractmethod
    def getData(self,*args):
        '''
        Downloads imaging data from server
        '''
        raise NotImplementedError()
    
    def __str__(self):
        return "The {} Server Object".format(self.name)


    #########################
    #    Query Builder      #
    #########################
    def otherRC3(self,ra,dec,margin):#survey): 
        '''
        Given ra,dec, pgc of an RC3 galaxy, use  Vizier to find a list of other rc3 that lies in the same margin field.
        in the form including the original galaxy of interest

        [['PGC54', 0.158083, 28.384556], ['PGC58', 0.183333, 28.401444]]

        Units
        =====
        Search radius (radius): arcsecond
        Search box (size): arcsecond
        '''
        # if (survey.name=='2MASS'):
        #     catalog = 'fp_xsc' #Default as extended source catalog
        # elif(survey.name=='WISE'):
        #     #prob 3 Cryo ?
        #     pass
        ##############
        #query = "spatial=box&catalog={}&size={}&outfmt=1&objstr={},{}".format(catalog,str(margin),str(ra),str(dec))
        rc3Cat = Vizier(catalog='VII/155/rc3')
        pos = FK5(ra*u.deg,dec*u.deg)
	#pos = coordinates.SkyFrame(ra*u.deg, dec*u.deg, frame='fk5')
#	pos =SkyCoord(ra* u.deg,dec* u.deg, frame='fk5')
        # print(pos)
        rc3_matches=rc3Cat.query_region(pos, radius=2*margin*u.deg)
        # print (rc3_matches[0])
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
        
    @abstractmethod
    def surveyFieldConverter(self,ra,dec,clean,*args):
        '''
        Returns which field the object lies in the survey
        the output and implementation of this method is hihgly dependent on survey structure
        Note: even though "clean" is optional, the parameter field stil needs to be written in to conform to method calls in rc3.py
        
        ex) SDSS => run,camcol,field
            2MASS => Tiles designation
        '''
        raise NotImplementedError()

