import montage_wrapper as montage
from astropy.io import fits as pyfits
import os
import shutil
from math import trunc
import sqlcl
import sys 
import fnmatch
# Assume you are inside directory (rfits/) where you have pulled all the g band fit files 
# find . -name "SDSS_r_*.fits" -type f -exec cp {} ./rfits \; 

def mosaic_band(band,ra,dec,margin,radius,pgc):#,clean=True):
    '''
    Input: source info param
    Create a mosaic fit file for the specified band.
    Return: String filename of resulting mosaic
    '''
    print ("------------------mosaic_band----------------------")
    DEBUG = True
    output = open("rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
    unclean = open("rc3_galaxies_unclean","a")
    filename = "{},{}".format(str(ra),str(dec))
    if (DEBUG) : print ("Querying data that lies inside margin")
    result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  ra between {0}-{1} and  {0}+{1}and dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))).readlines()
    clean_result = sqlcl.query( "SELECT distinct run,camcol,field FROM PhotoObj WHERE  CLEAN =1 and ra between {0}-{1} and  {0}+{1}and dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))) .readlines()
    clean = True
    print (result)
    if len(result)!=len(clean_result):
        print ("Data contain unclean images")
        clean=False
        unclean.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),pgc))    
    data =[]
    count =0
    for i in result:
        if count>1:
            list =i.split(',')
            list[2]= list[2][:-1]
            data.append(list)
        count += 1 
    print (data)
    if len(data)==0:
        if (DEBUG): print ('The given ra, dec of this galaxy does not lie in the SDSS footprint. Onto the next galaxy!')#Exit Program.'
        output.write(str(ra)+ "     "+ str(dec)+"     "+str(radius)+"\n")
        output.write("{}     {}     {}     {} \n".format(str(ra),str(dec),str(radius),pgc))
        #sys.exit()
        return -1 #special value reserved for not in SDSS footprint galaxies
    else :
        if (DEBUG): 
            print ( "Complete Query. These data lies within margin: ")
            print (data)
    # os.mkdir(filename)
    # os.chdir(filename)
    os.mkdir(band)
    os.chdir(band)
    os.mkdir ("raw")
    os.mkdir ("projected")
    os.chdir("raw")
    if (DEBUG): print ("Retrieving data from SDSS SAS server for "+ band +"band")
    for i in data :  
        out = "frame-{}-{}-{}-{}".format(str(band),str(i[0]).zfill(6),str(i[1]),str(i[2]).zfill(4))
        os.system("wget http://mirror.sdss3.org/sas/dr10/boss/photoObj/frames/301/{}/{}/{}.fits.bz2".format(str(i[0]),str(i[1]),out) )
        os.system("bunzip2 {}.fits.bz2".format(out))
    os.chdir("../")
    if (DEBUG) : print("Creating mosaic for {} band.".format(band))
    montage.mImgtbl("raw","images.tbl")
    montage.mHdr("{} {}".format(str(ra),str(dec)),margin,"{}.hdr".format(out))
    if (DEBUG): print ("Reprojecting images")
    os.chdir("raw")
    montage.mProjExec("../images.tbl","../"+out+".hdr","../projected", "../stats.tbl") 
    os.chdir("..")
    montage.mImgtbl("projected","pimages.tbl")
    os.chdir("projected")
    montage.mAdd("../pimages.tbl","../"+out+".hdr","SDSS_"+out+".fits")
    outfile_r="SDSS_{}_{}_{}r.fits".format(band,str(ra),str(dec))
    montage.mSubimage("SDSS_"+out+".fits",outfile_r,ra,dec,2*margin) # mSubImage takes xsize which should be twice the margin (margin measures center to edge of image)
    shutil.move(outfile_r,os.getcwd()[:-11] )#if change to :-11 then move out of u,g,r,i,z directory, may be more convenient for mJPEG
    if (DEBUG) : print ("Completed Mosaic for " + band)
    os.chdir("../..")
    hdulist = pyfits.open(outfile_r)
    hdulist[0].header['RA']=ra
    hdulist[0].header['DEC']=dec
    hdulist[0].header['RADIUS']=radius
    hdulist[0].header['PGC']=pgc
    hdulist[0].header['NED']=("http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname="+hdulist[0].header['PGC']+"&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES")
    hdulist[0].header['CLEAN']=clean
    hdulist[0].header['MARGIN']=margin
    outfile="SDSS_{}_{}_{}.fits".format(band,str(ra),str(dec))
    if (os.path.exists(outfile)):
        os.system("rm "+ outfile)
    hdulist.writeto(outfile)
    os.system("rm "+outfile_r)
    os.system("rm -r "+band+"/")
    print ("Completed Mosaic")
    return outfile 



def source_info(r_fits_filename):
    '''
    [ra,dec,margin,radius,pgc] ==> Is margin info necessary(?) YES
    Input: Filename String of R band Mosaic fit file
    Returns the updated [ra,dec,margin,radius,pgc] info about the identified RC3 source as a list
    If no RC3 source is identified then ['@','@',margin_value,'@','@'] is returned
    If RC3 lie outside of SDSS footprint then [-1,-1,-1,-1,-1] is returned
    '''
    print ("------------------source_info----------------------")
    file = r_fits_filename 
    print("Source info for {}".format(file))
    if (file ==-1): #special value reserved for not in SDSS footprint galaxies
        return [-1,-1,-1,-1,-1]
    hdulist = pyfits.open(file)
    rc3_ra= hdulist[0].header['RA']
    rc3_dec= hdulist[0].header['DEC']
    rc3_radius = hdulist[0].header['RADIUS']
    margin = hdulist[0].header['MARGIN']
    pgc = hdulist[0].header['PGC']
    os.system("sex {} -c default.sex".format(file))
    catalog = open("test.cat",'r')
    #Creating a list of radius
    radius = []
    for line in catalog:
        if (line[0]!='#'):
            radius.append(float(line.split()[1]))
    print (radius)
    #special value that indicate empty list (no object detected by SExtractor)
    radii='@'
    new_ra='@'
    new_dec='@'
    catalog = open("test.cat",'r')
    # Find max radius and treat as if it is rc3
    #Will have to modify this later to account for multiple neighboring large galaxies
    # Maybe by imposing other RC3-like characteristics (brightness..etc?)
    for i in catalog:
        line = i.split()
        if (line[0]!='#'  and float(line[1])==max(radius)): 
            print ('Biggest Galaxy with radius {} pixels!'.format(line[1]))
            radii = line[1]
            new_ra= line[2]
            new_dec = line[3]
    # print (len(radius)!=0)
    # print (radii!='@')
    if (len(radius)!=0 and radii!='@' and float(radii)>4.):
        #treating anything that is 4 pixel or greater as galaxy of interest.
        #radii : pixel to degree conversion
        radii = 0.00010995650106797878*float(radii)
        print ("Radii: {} degrees".format(str(radii)))
        print ("rc3: {} , updated: {} ".format(rc3_ra, new_ra))
        print ("rc3: {} , updated: {} ".format(rc3_dec,new_dec))
        print ("rc3: {} , updated: {} ".format(rc3_radius,radii))
        updated.write("{}       {}      {}      {}      {} \n".format(rc3_ra,rc3_dec,new_ra,new_dec,radii))
        mosaic_all_bands(new_ra,new_dec,margin,radii,pgc)
        return [new_ra,new_dec,margin,radii,pgc] 
        # margin was already set as 6*rc3_radius during initial_run
        # all additional mosaicking steps shoudl be 1.5 times this 
    else: 
        print ("No detected RC3 sources in image. Mosaic using a larger margin")
        # original automated mosaic program default 6*radius
        # call on mosaic program with +50% original margin
        r_mosaic_filename = mosaic_band('r',rc3_ra,rc3_dec,1.5*margin,rc3_radius,pgc)
        source_info(r_mosaic_filename)
        #mosaic_band('r',rc3_ra,rc3_dec,1.5*margin, radius, pgc)
        return ['@','@',1.5*rc3_radius,'@','@']
    #print (radius,new_ra,new_dec)

#Unit Tested : Sucess
def mosaic_all_bands(ra,dec,margin,radius,pgc):
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
        mosaic_band(band,ra,dec,margin,radius,pgc)
        #os.chdir("../")
    os.system("stiff  SDSS_i_{0}_{1}.fits  SDSS_r_{0}_{1}.fits SDSS_g_{0}_{1}.fits  -c stiff.conf  -OUTFILE_NAME  SDSS_{0}_{1}_BEST.tiff -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 ".format(str(ra),str(dec)))
    # Image for emphasizing low-surface sturcture
    os.system("stiff  SDSS_i_{0}_{1}.fits  SDSS_r_{0}_{1}.fits SDSS_g_{0}_{1}.fits  -c stiff.conf  -OUTFILE_NAME  SDSS_{0}_{1}_LOW.tiff  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8 ".format(str(ra),str(dec)))  
    os.system("rm stiff.xml")
    os.chdir("../")
    print ("Completed Mosaic")
    
#Unit Tested : Sucess
def initial_run ():
    '''
    Input : void
    Create r mosaic_band fit files for source_info to work on 
    initial_run should only be ran once at the begining of the program
    Output: r band mosaic fits for all galaxies below '@' inside rc3_ra_dec_diameter_pgc.txt
    Return: void
    '''
    print ("------------------initial_run----------------------")
    n = 0
    start=False
    output = open("rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
    unclean = open("rc3_galaxies_unclean","a")
    with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
        for line in f:
            print (line)
            a = str(line)[0]
            if a[0] =="@": #Debugging purpose, put this in the rc3(final).txt to start from where you left off (when error)
                start=True
                print ("Now start")
                continue
            if (start):
                n +=1
                ra = float(line.split()[0])
                dec = float(line.split()[1])
                radius = float(line.split()[2])/2. #radius = diameter/2
                pgc=str(line.split()[3]).replace(' ', '')
                clean=True
                filename = "{},{}".format(str(ra),str(dec))
                print ("Working on {}th RC3 Galaxy at {}".format(str(n),filename))
                # Run mosaic on r band with all original rc3 catalog values
                mosaic_band('r',ra,dec,2*radius,radius,pgc)

if __name__ == "__main__":            
    initial_run()
    updated = open("rc3_updated.txt",'a') # 'a' for append #'w')
    updated.write("ra       dec         new_ra      new_dec         radius \n")
    os.chdir("..")
    rfits=[file for root, dir, files in os.walk("rfits") for file in files if fnmatch.fnmatchcase(file, "SDSS_r_*.fits")]
    os.chdir("rfits/")
    for file in rfits:
        print(file)
        hdulist = pyfits.open(file)
        rc3_ra= hdulist[0].header['RA']
        rc3_dec= hdulist[0].header['DEC']
        rc3_radius= hdulist[0].header['RADIUS']
        pgc = hdulist[0].header['PGC']
        margin = hdulist[0].header['MARGIN']
        # you feed in the r fit mosaic from the initial run and let the recursion in source_info run wild
        info = source_info(file) 
        # If you trust recursion, you will magically get the final updated value here
        print ("Final updated params : "+str(info))
        # iteration =0
        # while (info[0]==info[1]==info[3]==info[4]=='@' ): 
        # # While RC3 no RC3 is identified inside field.
        #     if (iteration <=2):
        #         margin = float(info[2])
        #         print("#################################################")
        #         print ("No identified RC3 inside field. Mosaic with +50% margin")
        #         # r = mosaic_band('r',rc3_ra,rc3_dec,1.5*margin,rc3_radius,pgc)
        #         # recursive call that spits back final rc3 values
        #         r = source_info( )
        #         break #break out of while loop and mosaic_all_bands
        #     else:
        #         print("Can not identify RC3 source anywhere nearby")
        #         return # exit out of function (don't do mosaic_all_bands)
        #         #Perhaps, write these galaxies into a separate file??
        #     iteration +=1
        # mosaic_all_bands(ra,dec,margin,radius,pgc)
        # #final mosaic (g,r,i color)

        # hdulist = pyfits.open(r)
        # rc3_ra= hdulist[0].header['RA']
        # rc3_dec= hdulist[0].header['DEC']
        # rc3_radius= hdulist[0].header['RADIUS']
        # pgc = hdulist[0].header['PGC']
        # margin = hdulist[0].header['MARGIN']
        # info = source_info(file)
        # print (info)
        # iteration =0
        # rc3_radius = hdulist[0].header['RADIUS']