#!PATH=/usr/bin/:/data/small/des/montage/montage/Montage_v3.3/bin/:/bin
# RC3 Class is the core mosaicing class. Each RC3 galaxy is represented by an RC3 object.
# from catalog import Catalog
from rc3Catalog import RC3Catalog
from sdss import SDSS
from twoMass import TwoMass
import montage_wrapper as montage
from astropy.io import fits as pyfits
import os
import shutil
from math import trunc
import sqlcl
import sys 
import fnmatch
import numpy as np
import heapq
import time

class RC3(RC3Catalog):
    def __init__(self, rc3_ra, rc3_dec,rc3_radius,pgc, num_iterations=0):
        # initial rc3 ra ,dec,margin should be passed in as a attribute to the object
        self.rc3_ra = rc3_ra
        self.rc3_dec  = rc3_dec
        self.rc3_radius = rc3_radius
        # Patching up for a particular object with strange pgc only in the RC3 Catalog
        if (pgc=='6186a+b'):
            pgc='6186'      
        self.pgc = int(pgc)        
        self.num_iterations = num_iterations
        #updated positions
        self.new_ra='@'
        self.new_dec='@'

    def mosaic_band(self,band,ra,dec,margin,radius,pgc,survey):#,clean=True):
        '''
        Input: source info param
        Create a mosaic fit file for the specified band.
        Return: String filename of resulting mosaic
        '''
        print ("------------------mosaic_band----------------------")
        DEBUG = True
        output = open("../rc3_galaxies_outside_{}_footprint".format(survey.name),'a') # 'a' for append #'w')
        unclean = open("../rc3_galaxies_unclean_{}".format(survey.name),"a")
        # filename = "{},{}".format(str(ra),str(dec))
        filename = str(ra)+str(dec)
        #print (margin/radius)
        if (DEBUG) : print ("Querying data that lies inside margin")
        print (ra,dec,margin)
        #result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{1} and  {0}+{1}and dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))).readlines()
        result = survey.data_server.surveyFieldConverter(float(ra),float(dec),float(margin))
        clean_result = survey.data_server.surveyFieldConverter(float(ra),float(dec),float(margin),True)
        clean = True
        print ("result: "+str(result))
        print ("clean_result: "+str(clean_result))
        
        if (len(result)!=len(clean_result)and band=='u'):
            #only print this once in the u band. 
            #If it is unclean in u band (ex. cosmic ray, bright star..etc) then it must be unclean in the other bands too.
            print ("Data contain unclean images")
            clean=False
            unclean.write("{}     {}     {}     {} \n".format(self.rc3_ra,self.rc3_dec,self.rc3_radius,self.pgc))

        if (len(result)==0):             
            if (DEBUG): print ('The given ra, dec of this galaxy does not lie in the survey footprint. Onto the next galaxy!')#Exit Program.'
            # if (band=='r'):
                # not-in-footprint only written when mosaicing first (i.e. r) band
                # this is only relavant in the case where we call mosaic_band by mosaicAll 
                # since if you are only mosaicing one galaxy then this print statement is spit back.
            output.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),str(pgc)))
            return -1 #special value reserved for not in survey footprint galaxies
        else :
            if (DEBUG): 
                print ( "Complete Query. These data lies within margin: ")
                print (result)

        os.mkdir(band)
        os.chdir(band)
        os.mkdir ("raw")
        os.mkdir ("projected")
        os.chdir("raw")
        if (DEBUG): print ("Retrieving data from server for "+ band +"band")
        out=""
        for i in result :  
            if (survey.data_server.name=='Gator'):
                survey.data_server.getData(band,ra,dec,margin,survey)
                out = i #designation
                print out
            elif (survey.data_server.name=='SkyServer'):
                survey.data_server.getData(band,str(i[0]), str(i[1]),str(i[2]))
                out = "frame-"+str(band)+"-"+str(i[0]).zfill(6)+"-"+str(i[1])+"-"+str(i[2]).zfill(4)

        os.chdir("../")
        
        if (DEBUG) : print("Creating mosaic for "+band+" band.")
        outfile_r = "{}_{}_{}_{}r.fits".format(survey.name,band,ra,dec)
        outfile = "{}_{}_{}_{}.fits".format(survey.name,band,ra,dec)

        if (len(result)==1):
            #With header info, len of processed result list is 1 if there is only 1 field lying in the margin, simply do mSubImage without mosaicing
            #This patch should not be necessary but the program is aparently not mosaicing for the case where there is only one field.
            print ("Only one field in region of interest")
            os.chdir("raw")
            try:
                montage.mSubimage(out+".fits",outfile,ra,dec,2*margin) # mSubImage takes xsize which should be twice the margin (margin measures center to edge of image)
            except(montage.status.MontageError):
                print ("montage_wrapper.status.MontageError: mSubimage: Region outside image.")
                try :#give it one last chance
                    montage.mSubimage(out+".fits",outfile,ra,dec,margin)
                except(montage.status.MontageError):
                    print("Doesn't work after trying half the margin, just keep the raw FITS file")
                    # And continue source infoing, don't mask as not in footprint
                    if (os.path.exists("../../{}".format(outfile))):
                        os.system("rm -r {}".format("../../{}".format(outfile)))
                    shutil.move(outfile,"../..")
                    os.chdir("../../")
                    os.system("rm -r {}".format(survey.best_band))
                    return outfile
                print (os.getcwd())
                os.chdir("../../") #Get out of directory for that galaxy and move on
                os.system("rm -r {}".format(survey.best_band))
                print(os.getcwd())
                failed_msubimage = open ("failed_msubimage","a")
                failed_msubimage.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),str(pgc)))
                return -1 # masking with special value reserved for not in survey footprint galaxies
        
            hdulist = pyfits.open(outfile)
            if (os.path.exists("../../"+outfile)):
                os.system("rm ../../"+outfile)
            shutil.move(outfile,"../..")
            os.chdir("../..")
        else:
            montage.mImgtbl("raw","images.tbl")
            montage.mHdr(str(ra)+" "+str(dec),margin,out+".hdr")
            if (DEBUG): print ("Reprojecting images")
            os.chdir("raw")
            print(os.getcwd())
            montage.mProjExec("../images.tbl","../"+out+".hdr","../projected", "../stats.tbl")#,debug=True) 
            if os.listdir("../projected") == []: 
                print "Projection Failed. No projected images produced. Skip to the next galaxy" 
                os.chdir("../../") #Get out of directory for that galaxy and move on
                os.system("rm -r {}".format(survey.best_band))
                failed_projection = open ("failed_projection","a")
                failed_projection.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),str(pgc)))
                return -1 # masking with special value reserved for not in survey footprint galaxies
            os.chdir("..")
            montage.mImgtbl("projected","pimages.tbl")
            os.chdir("projected")
            montage.mAdd("../pimages.tbl","../"+out+".hdr","{}_{}.fits".format(survey.name,out))
            montage.mSubimage("{}_{}.fits".format(survey.name,out),outfile_r,ra,dec,2*margin) # mSubImage takes xsize which should be twice the margin (margin measures center to edge of image)
            shutil.move(outfile_r,os.getcwd()[:-11] )#if change to :-11 then move out of u,g,r,i,z directory, may be more convenient for mJPEG
            if (DEBUG) : print ("Completed Mosaic for " + band)
            os.chdir("../..")
            hdulist = pyfits.open(outfile_r)

        hdulist[0].header['RA']=ra
        hdulist[0].header['DEC']=dec
        hdulist[0].header['RADIUS']=radius
        hdulist[0].header['PGC']=pgc
        hdulist[0].header['NED']=("http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname="+ str(hdulist[0].header['PGC'])+"&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES")
        hdulist[0].header['CLEAN']=clean
        hdulist[0].header['MARGIN']=margin

        if (os.path.exists(outfile)):
            os.system("rm "+ outfile)
        hdulist.writeto(outfile)
        if (os.path.exists(outfile_r)):
            os.system("rm "+outfile_r)
        os.system("rm -r {}".format(band))
        print ("Completed Mosaic")
        return outfile 

    def source_info(self,r_fits_filename,survey):
        '''
        [ra,dec,margin,radius,pgc] ==> Is margin info necessary(?) YES
        Input: Filename String of R band Mosaic fit file
        Returns the updated [ra,dec,margin,radius,pgc] info about the identified RC3 source as a list
        If no RC3 source is identified then ['@','@',margin_value,'@','@'] is returned
        If RC3 lie outside of survey footprint then [-1,-1,-1,-1,-1] is returned
        '''
        # try:
        updated = open("rc3_updated.txt",'a') 
        self.num_iterations +=1
        print ("{}th iteration".format(self.num_iterations))
        if (self.num_iterations <= 3): #5 is too much
            print ("------------------source_info----------------------")
            file = r_fits_filename 
            print("Source info for {}".format(file))
            if (file ==-1): #special value reserved for not in survey footprint galaxies
                return [-1,-1,-1,-1,-1]
            try:
                # Try writing , if not then just pass. 
                # Key Error in the case when raw FITS from survey, not mosaiced by us.
                print("Trying to write info into fits file")
                # File info 
                hdulist = pyfits.open(file)
                rc3_ra= hdulist[0].header['RA']
                rc3_dec= hdulist[0].header['DEC']
                rc3_radius = hdulist[0].header['RADIUS']
                margin = hdulist[0].header['MARGIN']
                pgc = hdulist[0].header['PGC']
            except(KeyError):
                print("keyword not found")
                rc3_ra = self.rc3_ra
                rc3_dec = self.rc3_dec
                rc3_radius = self.rc3_radius
                margin = 2*self.rc3_radius
                pgc = self.pgc
                pass
            # Source Extraction
            # Remember to switch to "sextractor" for Ubuntu/ Linux, "sex" for Mac
            os.system("sex {} -c {}.sex".format(file,survey.name))
            # A list of other RC3 galaxies that lies in the field
            # In the case of source confusion, find all the rc3 that lies in the field.
            # other_rc3s = sqlcl.query("SELECT distinct rc3.ra, rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{1} and  {0}+{1} and po.dec between {2}-{3} and  {2}+{3}".format(str(rc3_ra),str(margin),str(rc3_dec),str(margin))).readlines()
            other_rc3s = survey.data_server.otherRC3(rc3_ra,rc3_dec,margin)#,survey)
            other_rc3s_info=other_rc3s
            print (other_rc3s)
            print ("ra,dec of catalog sources")
            #This list contains [pgc,ra,dec] as strings
            # Cutting away PGC information ,convert string to float 
            other_rc3s=[[int(lst[0][3:]),float(lst[1]),float(lst[2])] for lst in other_rc3s]
            # print(other_rc3s)
            # rc3_data = map (np.array,other_rc3s)
            rc3_data = other_rc3s
            print ("rc3_data: "+str(rc3_data))
            other_rc3s=[np.array([float(lst[1]),float(lst[2])]) for lst in other_rc3s]
            distances=[]
            for i in range(len(other_rc3s)-1):#len(data)//2):
                if (len(other_rc3s)>1 ): #odd number (unpaired) RC3s that lie in the field is ignored for now 
                # (but we have to take it into consideration eventually)
                # and len(data)%2==0
                    d2p= np.array(other_rc3s[i])-np.array(other_rc3s[i+1])
                    print ("d2p: {}".format(d2p))
                    distances.append(d2p)       
            # if(len(distances)!=0):
                
            if (len(distances)>1):
                print ("More than 2 galaxies inside field!")   
                print (distances)
                          
            #Conduct pairwise comparison
            catalog = open("test.cat",'r')
            #Creating a list of radius
            radius_list = []
            # Creating a corresponding list of ra,dec
            sextract_dict ={}
            for line in catalog:
                line = line.split()
                if (line[0]!='#'):
                    radius=np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2
                    radius_list.append(radius)
                    coord = np.array([float(line[2]),float(line[3])])
                    sextract_dict[radius]=coord
            print ("Radius: "+str(radius_list))
            if (len(sextract_dict)>0):
                #special value that indicate empty list (no object detected by SExtractor)
                radii='@'
                new_ra='@'
                new_dec='@'
                # catalog = open("test.cat",'r')
                n=-1
                if (len(distances)!=0):
                    # if there is source confusion, then we want to keep the nth largest radius
                    print ("Source Confusion")
                    n=len(distances)+1
                    print ("sextract_dict:"+str(sextract_dict))
                    print ("N-th largest radius:"+str(heapq.nlargest(n,sextract_dict)))
                    #nth largest radius
                    nth_largest=heapq.nlargest(n,sextract_dict)
                    sextract=[]
                    for i in heapq.nlargest(n,sextract_dict):
                        sextract.append(np.array(sextract_dict[i]))
                    print ("sextract:"+str(sextract))
                    # radius
                    nth_largest=[i for i in nth_largest if float(i)>15.]
                    print(nth_largest)
                    if(len(nth_largest)!=0):
                        radii = nth_largest[0]
                    #Coordinate matching by pairs
                    diff = []
                    #all possible coordinate pairs 
                    coord_match=[]
                    for i in other_rc3s : 
                        #determine shift vector 
                        for j in sextract:
                            print (str(i)+" " +str(j))
                            coord_match.append([i,j])
                            diff.append((j-i).tolist())  
                    print ("coord_match: "+str(coord_match))     
                    print ("diff: "+str(diff))
                    abs_diff = map (lambda x : map(lambda y:abs(y), x), diff)        
                    print ("abs_diff: "+str(abs_diff))
                    tmp = heapq.nsmallest(n,abs_diff)
                    print ("tmp : "+str(tmp))
                    # Bascially doing this , the long way, becasuse Python apparently can not do list -by element comparison and complains
                    #inx=abs_diff.index(np.array(i))
                    inx=[]
                    for i in tmp:
                        for j in abs_diff:
                            if (i==j):
                                print (abs_diff.index(j))
                                inx.append(abs_diff.index(j))
                    print (inx)
                    matched=[]
                    for i in inx:
                        print coord_match[i]
                        matched.append(coord_match[i])
                    print (other_rc3s_info)
                    info ={}
                    for i in other_rc3s_info:
                        pgc = int(i[0][3:])
                        ra= float(i[1])
                        dec= float(i[2])
                        info[pgc]= [ra,dec]
                    print ("info"+str(info))
                    print ("The galaxy that we want to mosaic is: "+str(info[self.pgc]))
                    new_ra= info[self.pgc][0]
                    new_dec = info[self.pgc][1]
                else:
                    print ("Source is Obvious")
                    n=1 # if no source confusion then just keep the maximum radius
                    #Creating a list of radius
                    radius = []
                    for line in catalog:
                        #print (line)
                        line = line.split()
                        if (line[0]!='#'):
                            radius.append(np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2)
                    #special value that indicate empty list (no object detected by SExtractor)
                    radii='@'
                    new_ra='@'
                    new_dec='@'
                    # If there is no other RC3 in the field, it means the largest galaxy in the field is the RC3 we are interested in
                    # So find max radius and treat as if it is rc3
                    for i in catalog:
                        line = i.split()
                        if (line[0]!='#' ):
                            #Pythagorean method
                            radii = np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2
                            if (radii==max(radius)):
                                print ('Biggest Galaxy with radius {} pixels!'.format(str(radii)))
                                radii = radii
                                new_ra= line[2]
                                new_dec = line[3]
                                break
                print ("new_ra and new_dec: {} , {}  ".format(str(new_ra),str(new_dec)))
                if (radii!='@' and float(radii)>15): # There exist 1 or more detected source
                    print ("Radii: {} pixel".format(str(radii)))
                    radii = 0.00010995650106797878*radii #pixel to degree conversion
                    print ("Radii: {} degrees".format(str(radii)))
                    print ("rc3: {} , updated: {} ".format(rc3_ra, new_ra))
                    print ("rc3: {} , updated: {} ".format(rc3_dec,new_dec))
                    print ("rc3: {} , updated: {} ".format(rc3_radius,radii))
                    updated.write("{}       {}       {}       {}       {}       {} \n".format(rc3_ra,rc3_dec,new_ra,new_dec,radii, pgc))
                    self.mosaic_all_bands(new_ra,new_dec,margin,radii,pgc,survey)
                    return [float(new_ra),float(new_dec),margin,radii,pgc] 
                    # margin was already set as 2*rc3_radius during the first run
                    # all additional mosaicking steps shoudl be 1.5 times this 
                #else: #radii =@ if all SExtracted radius is <15 
            print ("No detected RC3 sources in image. Mosaic using a larger margin")
            r_mosaic_filename = self.mosaic_band(survey.best_band,rc3_ra,rc3_dec,1.5*margin,rc3_radius,pgc,survey)
            self.source_info(r_mosaic_filename,survey)
            return ['@','@',1.5*margin,'@','@']
        else : # no detection since exceed num_iteration
            no_detection = open("../no_detected_rc3_candidate_nearby.txt",'a') # 'a' for append #'w')
            #no_detection.write("rc3_ra       rc3_dec        rc3_radius        pgc \n")
            no_detection.write("{}       {}        {}        {} \n".format(self.rc3_ra,self.rc3_dec,self.rc3_radius,self.pgc))
        # except (IOError):
        #     print ("File Not Found Error, if rfits is not found then mosaic an rfits")
        #     rfits=self.mosaic_band('r',self.rc3_ra,self.rc3_dec,3*self.rc3_radius,self.rc3_radius,self.pgc,survey)
        #     #Should I do source_info here again or autodetect??
        #     # self.source_info(rfits,survey)
        # except:
        #     print("Something went wrong when mosaicing PGC{}, just ignore it and keep mosaicing the next galaxy".format(str(pgc)))
        #     error = open ("sourceinfo_error.txt","a")
        #     error.write("{}       {}        {}        {} \n".format(self.rc3_ra,self.rc3_dec,self.rc3_radius,self.pgc))
        #     return['x','x','x','x','x']
            
    #Unit Tested : Sucess
    def mosaic_all_bands(self,ra,dec,margin,radius,pgc,survey):
        '''
        Input
        Creates u,g,r,i,z fit file mosaic and g,r,i color images.
        Call this on the final step of the program,
        once we have verified that the RC3 source lies 
        inside the new margin and updated center ra,dec and radii
        Return void
        '''
        print ("------------------mosaic_all_bands----------------------")
        filename = "{},{}".format(str(ra),str(dec))
        os.mkdir(filename)
        os.chdir(filename)
        bands =survey.bands #['u','g','r','i','z']
        for band in bands:
            self.mosaic_band(band,ra,dec,margin,radius,pgc,survey)
            #os.chdir("../")
        os.system("stiff  {2}_{5}_{0}_{1}.fits  {2}_{4}_{0}_{1}.fits {2}_{3}_{0}_{1}.fits  -c {6}.conf  -OUTFILE_NAME  {2}_{0}_{1}_BEST.tiff {7}".format(ra,dec,survey.name,survey.color_bands[0],survey.color_bands[1],survey.color_bands[2],survey.name,survey.stiff_param_low))
        # Image for emphasizing low-surface sturcture
        os.system("stiff  {2}_{5}_{0}_{1}.fits  {2}_{4}_{0}_{1}.fits {2}_{3}_{0}_{1}.fits  -c {6}.conf  -OUTFILE_NAME  {2}_{0}_{1}_LOW.tiff  {7}".format(ra,dec,survey.name,survey.color_bands[0],survey.color_bands[1],survey.color_bands[2],survey.name,survey.stiff_param_best)) 
        if (not(os.path.exists("stiff.xml"))):
            #If stiff file exist then it means stiff run is sucessful
            #sometimes stiff doesn't run because 
            #*Error*: Image width doesn't match in SDSS_g_0.1044948_+7.8537508.fits
            # I will just write these into a file and do post processing on them, they shouldn't be that many of them
            stiff_error = open("../stiff_error.txt",'a') # 'a' for append #'w')
            stiff_error.write("{}       {}        {}        {} \n".format(self.rc3_ra,self.rc3_dec,self.rc3_radius,self.pgc))
        # Deletion done in each single mosaic_band 
        # for band in bands:
        #     os.system("rm -r {}".format(band))
        os.system("rm stiff.xml")
        os.chdir("../")
        print ("Completed Mosaic")
  
