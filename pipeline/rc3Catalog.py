import os
from catalog import Catalog
class RC3Catalog(Catalog):
	'''
	Class for RC3 Catalog objects
	'''
	def __init__(self):
		self.name= 'Catalog'
		self.frame= 'fk5'
		self.equinox = 'J2000'
		self.allObj=self._initAllObj()

	def _initAllObj(self):
		'''
		Create a list of all objects inside the catalog
		'''
		from rc3 import RC3
		allObj=[]
		n = 0
		start=False
		output = open("rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
		unclean = open("rc3_galaxies_unclean","a")
		# survey=SDSS()
		
		with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
			for line in f:
	        	    #try:
	            #print (line)
				a = str(line)[0]
	            #Debugging purpose, put this in the rc3(final).txt to start from where you left off (when error)
				if a[0] =="@": 
					start=True
					continue
				if (start):
					n +=1
					ra = float(line.split()[0])
					dec = float(line.split()[1])
					radius = float(line.split()[2])/2. #radius = diameter/2
					pgc=str(line.split()[3]).replace(' ', '')
					clean=True
	                # filename = "{},{}".format(str(ra),str(dec))
					filename = str(ra)+str(dec)
	                #print ("Working on {}th RC3 Galaxy at {}".format(str(n),filename))
	                # Run mosaic on r band with all original rc3 catalog values
					obj= RC3(ra,dec,radius,pgc)
					allObj.append(obj)
		return allObj


	def mosaicAll(self,survey):
		'''
		survey : Survey object
		Produce all band FITS files and color mosaic for every objects inside the Catalog that lies within the footprint of the given survey
		'''   
		DEBUG = True
		updated = open("rc3_updated.txt",'a') # 'a' for append #'w')
		updated.write("ra       dec         new_ra      new_dec         radius \n")
		output = open("rc3_galaxies_outside_SDSS_footprint.txt",'a') # 'a' for append #'w')
		unclean = open("rc3_galaxies_unclean","a")
		for obj in self.allObj:
			#try:
			print("Working on PGC{}, at({} , {})".format(str(obj.pgc), str(obj.rc3_ra),str(obj.rc3_dec)))
			try:
				rfits=obj.mosaic_band('r',obj.rc3_ra,obj.rc3_dec,3*obj.rc3_radius,obj.rc3_radius,obj.pgc,survey)
				if(rfits!=-1): #Special value for outside footprint or error , no rfits produced
					obj.source_info(rfits,survey)
			except:
				print("Something went wrong in mosaicing PGC {}".format(str(obj.pgc)))
				if (os.getcwd()[18:]!='bulk_run2'):
				# if we are stuck inside some sort of position directory instead of our running directory. Must get out.
					print ("Get out of cwd")
					os.chdir("..")
				mosaicAll_error=open("mosaicAll_error","a")
				mosaicAll_error.write("{}       {}        {}        {} \n".format(str(obj.rc3_ra),str(obj.rc3_dec),str(obj.rc3_radius),str(obj.pgc)))
				pass
#       except:
                #               print("Something went wrong when mosaicing PGC{}, just ignore it and keep mosaicing the next galaxy".format(str(obj.pgc)))
                #               mosaicAll_error=open("mosaicAll_error","a")
                #               mosaicAll_error.write("{}       {}        {}        {} \n".format(obj.rc3_ra,obj.rc3_dec,obj.rc3_radius,obj.pgc))

	def mosaicAllDebug():
		'''
		Produce all band FITS files and color mosaic for every objects inside the Catalog that lies within the footprint of the given survey
		after the @ sign.
		'''

	def printAll(self):
		pass
