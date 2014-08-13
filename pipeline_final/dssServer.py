from  server import Server
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
        print ("querying: "+"wget {}http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder?{}{}".format(' "',query,'" '))
        
        os.system("wget -O result.txt {}http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder?{}{}".format(' "',query,'" '))

    def getData(self,band,ra,dec,margin):	
        '''
        Downloads imaging data from server
        URL query form : http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-im_sia?
        
        FORMAT image/fits
		Return URLs for image FITS files

		POS=ra,dec &SIZE = margin
        '''
 		# Margin value conversion degree to arcminute 1 degree = 60 arcminutes
 		# Can not specify band?
        q = "locstr={}+{}&survey=dss&mode=prog".format(ra,dec)#,60*margin)
        self.query(q)
        result = XMLparse(band,ra,dec,margin)
        filename = result[0]
        url = result[1]
        print ("result:{}".format(result))
        print ("Downloading "+filename)
        os.system("wget -O {} {}{}{} ".format(filename,' "',url,'" '))
    	# return i 
        #not typical of getData, but I want it to return the number of plates collected 
        #so that I could use this in  surveyFieldConverter

    #########################
    #    Query Builder		#
    ######################### 
    def surveyFieldConverter(self,ra,dec,margin,clean=True):
        '''
        for DSS return all the all-band PLATEID that lies in the search field 
        the all-band PLATEID is a string concatenation of all 5 PLATEID for the
        particular region of interest, one for each band of the DSS, so that it is 
        treated as one "basic imaging entity".
        '''
        lst = []
        #allbandPLATEID=""
        #only testing in the 1b band, assuming that if x photographic plates span the search area, than the same case goes for the other bands.
        q = "locstr={}+{}&survey=dss&mode=prog".format(ra,dec)#,60*margin)
        self.query(q)
        result = XMLparse("1r",ra,dec,margin)
        filename = result[0]
        i = result[2]
        # for i in ['1b','1r','2b','2r','2ir']:
        # 	filename = "DSS_{}_{}_{}.fits".format(band,ra,dec)
        # 	hdulist = pyfits.open(filename)
        # 	allbandPLATEID=allbandPLATEID+"_"+hdulist[0].header['PLATEID']
        # lst.append(allbandPLATEID)
        # # Remove all the files after obtaining info needed
        for n in range((i/5)+1):
        	# Fake name made by us
            lst.append("PhotoPlate{}".format(n))
        return lst


def XMLparse(band,ra,dec,margin):
    '''
    helper method that parse XML to find URL of all objects lying inside field 
    '''
    with open("result.txt") as f:
        n=0
        i=0
        url = " "
        filename=" "
        for line in f:
            # The URL is stored in the line  after <fitsurl>
            if (line.strip() =="<fitsurl>"): #or n==0):
                # passing till 1 lines down <fitsurl>
                n+=1
                pass
            elif (n==1):
                n=0
                # print ("here")
                url = line.split('[')[-1].split(']')[0].strip()
                print (url)
                if (i/5>1): # Assuming the highly unlikely case that there are more than 2 photographic plates spanning the search area
                    #preventing other downloads to override the initial file
                    #filename = "DSS_{}_{}_{}_{}.fits".format(band,str(ra),str(dec),str(i/5))
                    filename = "raw_{}_{}.fits".format(band,str(i/5))
                else:
                    #filename = "DSS_{}_{}_{}.fits".format(band,str(ra),str(dec))
                    filename = "raw_{}.fits".format(band)
                b = url.split("/")[-1][:-9]
                # print ("{},{}".format(b,i))
                # Assigning url to only Band Filters specified by param
                if ( band=='1b' and b=='poss1_blue' and i==0):
                    print('POSSIB')
                    break
                elif (band == '1r' and b=='poss1_red' and i ==1):
                    print ('POSSIR')
                    break
                elif (band == '2b' and b=='poss2ukstu_blue' and i ==2):
                    print('POSSIIB')
                    break
                elif (band == '2r' and b=='poss2ukstu_red' and i ==3):
                    print ('POSSIIR')
                    break
                elif (band == '2ir' and b=='poss2ukstu_ir' and i ==4):
                    print('POSSIIIR')
                    break
                i+=1
        print (filename)
        print (url)
        print (i)
        os.system("rm result.txt")
        return [filename,url,i]    


        
