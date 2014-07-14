# RC3 Class is the core mosaicing class. Each RC3 galaxy is represented by an RC3 object.
# from catalog import Catalog
from rc3Catalog import RC3Catalog
from sdss import SDSS
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
# Assume you are inside directory (rfits/) where you have pulled all the g band fit files 
# find . -name "SDSS_r_*.fits" -type f -exec cp {} ./rfits \; 

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
        output = open("../rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
        unclean = open("../rc3_galaxies_unclean","a")
        # filename = "{},{}".format(str(ra),str(dec))
        filename = str(ra)+str(dec)
        #print (margin/radius)
        if (DEBUG) : print ("Querying data that lies inside margin")
        #result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{1} and  {0}+{1}and dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))).readlines()
        result = survey.data_server.runCamcolFieldConverter(ra,dec,margin)
        clean_result = survey.data_server.runCamcolFieldConverter(ra,dec,margin,True)
        # result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between "+str(ra)+"-"+str(margin)+" and " +str(ra)+"+"+str(margin)+"and dec between "+str(dec)+"-"+str(margin)+" and "+ str(dec)+"+"+str(margin)).readlines()
        # clean_result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between "+str(ra)+"-"+str(margin)+" and " +str(ra)+"+"+str(margin)+"and dec between "+str(dec)+"-"+str(margin)+" and "+ str(dec)+"+"+str(margin)).readlines()
        # clean_result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between {0}-{1} and  {0}+{1}and dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))) .readlines()
        clean = True
        print (result)
        print (clean_result)
        
        if (len(result)>1):
            if (result[0][:6]=="<html>"):
                print("strange error from SQL server")
                return -1
            if (result[1]=='error_message\n' or clean_result[1]=='error_message\n'):
                #Case where doing more than 60 queries in 1 minute
                time.sleep(60)
                #results are messed up, need to re-query
                # result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between "+str(ra)+"-"+str(margin)+" and " +str(ra)+"+"+str(margin)+"and dec between "+str(dec)+"-"+str(margin)+" and "+ str(dec)+"+"+str(margin)).readlines()
                # clean_result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between "+str(ra)+"-"+str(margin)+" and " +str(ra)+"+"+str(margin)+"and dec between "+str(dec)+"-"+str(margin)+" and "+ str(dec)+"+"+str(margin)).readlines()
                result = survey.data_server.runCamcolFieldConverter(ra,dec,margin)
                clean_result = survey.data_server.runCamcolFieldConverter(ra,dec,margin,True)
        
        if (len(result)!=len(clean_result) and band=='u'):
            #only print this once in the u band. If it is unclean in u band (ex. cosmic ray, bright star..etc) then it must be unclean in the other bands too.
            print ("Data contain unclean images")
            clean=False
            unclean.write(str(ra)+"     "+str(dec)+"     "+str(radius)+"     "+str(pgc))
            # unclean.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),pgc))    
        # data =[]
        # count =0
        # for i in result:
        #     if count>1:
        #         list =i.split(',')
        #         list[2]= list[2][:-1]
        #         data.append(list)
        #     count += 1 
        # # print (data)
        # data=result
        if (len(result)==0 and band=='r'): #you will only evounter non-footprint galaxy inint run , because after that we just take the footprint gaalxy already mosaiced (init) from rfits
            if (DEBUG): print ('The given ra, dec of this galaxy does not lie in the SDSS footprint. Onto the next galaxy!')#Exit Program.'
            output.write(str(ra)+ "     "+ str(dec)+"     "+str(radius)+"\n")
            # output.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),pgc))
            output.write(str(ra)+"     "+str(dec)+"     "+str(radius)+"     "+str(pgc))
            #sys.exit()
            return -1 #special value reserved for not in SDSS footprint galaxies
        else :
            if (DEBUG): 
                print ( "Complete Query. These data lies within margin: ")
                print (result)
        # os.mkdir(filename)
        # os.chdir(filename)
        #if (os.path.exists(band)):
        #os.system("rm -r "+band)
        os.mkdir(band)
        os.chdir(band)
        os.mkdir ("raw")
        os.mkdir ("projected")
        os.chdir("raw")
        if (DEBUG): print ("Retrieving data from SDSS SAS server for "+ band +"band")
        for i in result :  
            out = "frame-"+str(band)+"-"+str(i[0]).zfill(6)+"-"+str(i[1])+"-"+str(i[2]).zfill(4)
            os.system("wget http://mirror.sdss3.org/sas/dr10/boss/photoObj/frames/301/"+str(i[0])+"/"+str(i[1])+"/"+out+".fits.bz2")
            os.system("bunzip2 "+out+".fits.bz2")
        os.chdir("../")
        if (DEBUG) : print("Creating mosaic for "+band+" band.")
        outfile_r="SDSS_"+band+"_"+str(ra)+"_"+str(dec)+"r.fits"
        outfile="SDSS_"+band+"_"+str(ra)+"_"+str(dec)+".fits"
        if (len(result)==1):
            #With header info, len of processed result list is 1 if there is only 1 field lying in the margin, simply do mSubImage without mosaicing
            #This patch should not be necessary but the program is aparently not mosaicing for the case where there is only one field.
            print ("Only one field in region of interest")
            os.chdir("raw")
            montage.mSubimage(out+".fits",outfile,ra,dec,2*margin) # mSubImage takes xsize which should be twice the margin (margin measures center to edge of image)
            #os.chdir("../..")
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
            montage.mProjExec("../images.tbl","../"+out+".hdr","../projected", "../stats.tbl") 
            os.chdir("..")
            montage.mImgtbl("projected","pimages.tbl")
            os.chdir("projected")
            montage.mAdd("../pimages.tbl","../"+out+".hdr","SDSS_"+out+".fits")
            # outfile_r="SDSS_{}_{}_{}r.fits".format(band,str(ra),str(dec))
            #outfile_r="SDSS_"+band+"_"+str(ra)+"_"+str(dec)+"r.fits"
            montage.mSubimage("SDSS_"+out+".fits",outfile_r,ra,dec,2*margin) # mSubImage takes xsize which should be twice the margin (margin measures center to edge of image)
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
        #print("Deleting")
        os.system("rm -r "+band+"/")
        print ("Completed Mosaic")
        return outfile 

    def source_info(self,r_fits_filename,survey):
        '''
        [ra,dec,margin,radius,pgc] ==> Is margin info necessary(?) YES
        Input: Filename String of R band Mosaic fit file
        Returns the updated [ra,dec,margin,radius,pgc] info about the identified RC3 source as a list
        If no RC3 source is identified then ['@','@',margin_value,'@','@'] is returned
        If RC3 lie outside of SDSS footprint then [-1,-1,-1,-1,-1] is returned
        '''
        #Create a survey object (generic)
        # s = Survey(survey)
        # (s.data_server)
        # survey_info = s.get_survey_info()
        try:
            updated = open("rc3_updated.txt",'a') 
            self.num_iterations +=1
            print ("{}th iteration".format(self.num_iterations))
            if (self.num_iterations < 3): #5 is too much
                print ("------------------source_info----------------------")
                file = r_fits_filename 
                print("Source info for {}".format(file))
                if (file ==-1): #special value reserved for not in SDSS footprint galaxies
                    return [-1,-1,-1,-1,-1]

            # File info 
                hdulist = pyfits.open(file)
                rc3_ra= hdulist[0].header['RA']
                rc3_dec= hdulist[0].header['DEC']
                rc3_radius = hdulist[0].header['RADIUS']
                margin = hdulist[0].header['MARGIN']
                pgc = hdulist[0].header['PGC']

                #Source Extraction
                os.system("sex {} -c default.sex".format(file))
                # A list of other RC3 galaxies that lies in the field
                # In the case of source confusion, find all the rc3 that lies in the field.
                # other_rc3s = sqlcl.query("SELECT distinct rc3.ra, rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{1} and  {0}+{1} and po.dec between {2}-{3} and  {2}+{3}".format(str(rc3_ra),str(margin),str(rc3_dec),str(margin))).readlines()
                other_rc3s = survey.data_server.otherRC3(rc3_ra,rc3_dec,margin)
                print (other_rc3s)

                # data =[]
                # count =0
                # for i in other_rc3s:
                #     if count>1:
                #         list =i.split(',')
                #         list[0] = float(list[0])
                #         list[1]= float(list[1][:-1])
                #         data.append(list)
                #     count += 1 
                print ("ra,dec of catalog sources")
                # rc3_data = map (np.array,data)
                rc3_data = map (np.array,other_rc3s)
                print ("rc3_data: "+str(rc3_data))
                # if (len(rc3_data)>0):
                # print ("here2")
                # data=other_rc3s
                distances=[]
                for i in range(len(other_rc3s)-1):#len(data)//2):
                    if (len(other_rc3s)>1 ): #odd number (unpaired) RC3s that lie in the field is ignored for now 
                    # (but we have to take it into consideration eventually)
                    # and len(data)%2==0
                        d2p= np.array(other_rc3s[i])-np.array(other_rc3s[i+1])
                        print ("d2p: {}".format(d2p))
                        distances.append(d2p)       
                if(len(distances)!=0):
                    print (distances)
                if (len(distances)>1):
                    print ("More than 2 galaxies inside field!")   
                print (distances)                           
                #Conduct pairwise comparison
                catalog = open("test.cat",'r')
                #Creating a list of radius
                radius_list = []
                # Creating a corresponding list of ra,dec
                #sextract = []
                sextract_dict ={}
                for line in catalog:
                    # print (line)
                    line = line.split()
                    if (line[0]!='#'):
                        # print("HERE!")
                        #sextract.append(np.array([line[2],line[3]]))
                        radius=np.sqrt((float(line[6])-float(line[4]))**2+(float(line[7])-float(line[5]))**2)/2
                        #print(radius)
                        radius_list.append(radius)
                        coord = np.array([float(line[2]),float(line[3])])
                        sextract_dict[radius]=coord
                print ("Radius: "+str(radius_list))
                print ("SExtract_dict: "+str(sextract_dict))
                if (len(sextract_dict)>0):
                    #special value that indicate empty list (no object detected by SExtractor)
                    radii='@'
                    new_ra='@'
                    new_dec='@'
                    catalog = open("test.cat",'r')
                    n=-1
                    if (len(distances)!=0):
                        # if there is source confusion, then we want to keep the nth largest radius
                        print ("Source Confusion")
                        n=len(distances)+1
                        print ("sextract_dict:")
                        print (sextract_dict)
                        print ("N-th largest radius:")
                        print(heapq.nlargest(n,sextract_dict))
                        #nth largest radius
                        nth_largest=heapq.nlargest(n,sextract_dict)
                        sextract=[]
                        for i in heapq.nlargest(n,sextract_dict):
                            sextract.append(np.array(sextract_dict[i]))
                        print ("sextract:")
                        print (sextract)

                        # radius
                        nth_largest=[i for i in nth_largest if float(i)>15.]
                        print(nth_largest)
                        if(len(nth_largest)!=0):
                            radii = nth_largest[0]

                        #Coordinate matching by pairs
                        diff = []
                        #all possible coordinate pairs 
                        coord_match=[]
                        for i in rc3_data : 
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
                                #print (i)
                                #print (j)
                                if (i==j):
                                    print (abs_diff.index(j))
                                    inx.append(abs_diff.index(j))
                        print (inx)
                        matched=[]
                        for i in inx:
                            print coord_match[i]
                            matched.append(coord_match[i])
                            # for j in coord_match:
                            #     print ([i,j])
                            #     if (all(np.array([1,2])==np.array([1,2])))
                            # #matches = [coord for coord in coord_match ]
                            # #print (matches)
                         #        print ("Matched coordinates: "+str(coord_match[inx]))

                        # # A list of other RC3 galaxies that lies in the field
                        # # other_rc3s = sqlcl.query("SELECT distinct rc3.pgc,rc3.ra,rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{1} and  {0}+{1} and po.dec between {2}-{3} and  {2}+{3}".format(str(rc3_ra),str(margin),str(rc3_dec),str(margin))).readlines()
                        # other_rc3s = survey.data_server.otherRC3(rc3_ra,rc3_dec,margin)
                        # print ("PGC of other_rc3s")
                        # # print (other_rc3s)

                        info ={}
                        count =0
                        for i in other_rc3s:
                            if count>1:
                                list =i.split(',')
                                pgc = int(list[0][6:])
                                ra= float(list[1][:-1])
                                dec= float(list[2][:-1])
                                info[pgc]= [ra,dec]
                            count += 1 
                        print (info)
                        print ("The galaxy that we want to mosaic is: "+str(info[self.pgc]))
                        new_ra= info[self.pgc][0]
                        new_dec = info[self.pgc][1]
                    else:
                        print ("Source is Obvious")
                        n=1 # if no source confusion then just keep the maximum radius
                        catalog = open("test.cat",'r')
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
                        catalog = open("test.cat",'r')
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
                        updated.write("{}       {}      {}      {}      {} \n".format(rc3_ra,rc3_dec,new_ra,new_dec,radii))
                        self.mosaic_all_bands(new_ra,new_dec,margin,radii,pgc,survey)
                        return [float(new_ra),float(new_dec),margin,radii,pgc] 
                        # margin was already set as 6*rc3_radius during initial_run
                        # all additional mosaicking steps shoudl be 1.5 times this 
                # else: #radii =@ if all SExtracted radius is <15 
                print ("No detected RC3 sources in image. Mosaic using a larger margin")
                # original automated mosaic program default 6*radius
                # call on mosaic program with +50% original margin
                r_mosaic_filename = self.mosaic_band('r',rc3_ra,rc3_dec,1.5*margin,rc3_radius,pgc,survey)
                self.source_info(r_mosaic_filename,survey)
                return ['@','@',1.5*margin,'@','@']
            else : 
                no_detection = open("../no_detected_rc3_candidate_nearby.txt",'a') # 'a' for append #'w')
                no_detection.write("rc3_ra       rc3_dec        rc3_radius        pgc \n")
                no_detection.write("{}       {}        {}        {} \n".format(self.rc3_ra,self.rc3_dec,self.rc3_radius,self.pgc))
        except (IOError):
            print ("File Not Found Error, if rfits is not found then mosaic an rfits")
            self.mosaic_band('r',self.rc3_ra,self.rc3_dec,3*self.rc3_radius,self.rc3_radius,self.pgc,survey)
            #Should I do source_info here again or autodetect??
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
        bands =['u','g','r','i','z']
        for band in bands:
            self.mosaic_band(band,ra,dec,margin,radius,pgc,survey)
            #os.chdir("../")
        os.system("stiff  SDSS_i_{0}_{1}.fits  SDSS_r_{0}_{1}.fits SDSS_g_{0}_{1}.fits  -c stiff.conf  -OUTFILE_NAME  SDSS_{0}_{1}_BEST.tiff -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 ".format(str(ra),str(dec)))
        # Image for emphasizing low-surface sturcture
        os.system("stiff  SDSS_i_{0}_{1}.fits  SDSS_r_{0}_{1}.fits SDSS_g_{0}_{1}.fits  -c stiff.conf  -OUTFILE_NAME  SDSS_{0}_{1}_LOW.tiff  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8 ".format(str(ra),str(dec)))  
        os.system("rm stiff.xml")
        os.chdir("../")
        # Move the finished rfit files outside so that, if terminate during the program, easier to recongnize which is already done and which is not.
        shutil.move("SDSS_r_{0}_{1}.fits".format(str(self.rc3_ra),str(self.rc3_dec)),"../finished_rfits")
        print ("Completed Mosaic")
  

# def mosaic_example(rc3_obj):
#     #Single example used for testing purposes so that we don't have to run the whole loop every time    
#     # intial run
#     #r_fit = rc3_obj.mosaic_band('r',rc3_obj.rc3_ra,rc3_obj.rc3_dec,3*rc3_obj.rc3_radius,rc3_obj.rc3_radius,rc3_obj.pgc) 
#     r_fit="SDSS_r_0.184583333333_28.4013888889.fits"
#     # Running source info is a comprehensive way of testing all other functions as well as the recursion
#     hdulist = pyfits.open(r_fit)
#     # rc3_ra= hdulist[0].header['RA']
#     # rc3_dec= hdulist[0].header['DEC']
#     # rc3_radius= hdulist[0].header['RADIUS']
#     # pgc = hdulist[0].header['PGC']
#     # margin = hdulist[0].header['MARGIN']
#     info = rc3_obj.source_info(r_fit,survey)
#     print (info)
 
# if __name__ == "__main__":            
#     DEBUG = True
#     updated = open("rc3_updated.txt",'a') # 'a' for append #'w')
#     updated.write("ra       dec         new_ra      new_dec         radius \n")
#     n = 0
#     start=False
#     output = open("rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
#     unclean = open("rc3_galaxies_unclean","a")
#     survey=SDSS()
#     with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
#         for line in f:
#             #try:
#             #print (line)
#             a = str(line)[0]
#             #Debugging purpose, put this in the rc3(final).txt to start from where you left off (when error)
#             if a[0] =="@": 
#                 start=True
#                 print ("Now start")
#                 continue
#             if (start):
#                 n +=1
#                 ra = float(line.split()[0])
#                 dec = float(line.split()[1])
#                 radius = float(line.split()[2])/2. #radius = diameter/2
#                 pgc=str(line.split()[3]).replace(' ', '')
#                 clean=True
#                 # filename = "{},{}".format(str(ra),str(dec))
#                 filename = str(ra)+str(dec)
#                 #print ("Working on {}th RC3 Galaxy at {}".format(str(n),filename))
#                 # Run mosaic on r band with all original rc3 catalog values
#                 obj= RC3(ra,dec,radius,pgc)
#                 rfits=obj.mosaic_band('r',ra,dec,3*radius,radius,pgc,survey)
#                 # os.system("rm ")
#                 if(rfits!=-1): #Special value for outside footprint or error , no rfits produced
#                     obj.source_info(rfits,survey)
#             #except :
#                 #print("Something went wrong when mosaicing PGC"+str(pgc)+", just ignore it and keep mosaicing the next galaxy")
#                 #error = open ("sourceinfo_error.txt","a")
#                 #error.write(str(ra)+"        "+str(dec)+"        "+str(radius)+"        "+str(pgc))
#                 #continue