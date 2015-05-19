import os
from catalog import Catalog
class RC3Catalog(Catalog):
	'''
	Class for RC3 Catalog objects
	'''
	def __init__(self):
		self.name= 'RC3 Catalog'
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

		with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
			for line in f:
				a = str(line)[0]
	            # Useful for debugging purpose, put this in the rc3_ra_dec_pgc.txt to start from where you left off (when error)
				if a[0] =="@": 
					start=True
					continue
				if (start):
					n +=1
					ra = float(line.split()[0])
					dec = float(line.split()[1])
					radius = float(line.split()[2])/2. #radius = diameter/2 [in degrees]
					pgc=str(line.split()[3]).replace(' ', '')
					clean=True
					obj= RC3(ra,dec,radius,pgc)
					allObj.append(obj)
		return allObj

	def initSubset(self,file):
	    '''
	    Create a list of all objects inside a user-defined catalog
	    '''
	    from rc3 import RC3
	    allObj=[]
	    n = 0
	    with open(file,'r') as f:
	        for line in f:
	            if (n>=1):
	                # new_ra = float(line.split()[5])
	                # new_dec = float(line.split()[6])
	                # radius = float(line.split()[4])/2. #radius = diameter/2
	                # pgc=int(line.split()[1])
	                ra = float(line.split()[0])
	                dec = float(line.split()[1])
	                radius = float(line.split()[2])/2. #radius = diameter/2
	                pgc=int(float(line.split()[3]))
	                clean=True
	                obj= RC3(ra,dec,radius,pgc)
	                allObj.append(obj)
	            n +=1
	    return allObj

	def mosaicAll(self,survey):
		'''
		survey : Survey object
		Produce all band FITS files and color mosaic for every objects inside the Catalog that lies within the footprint of the given survey
		'''   
		DEBUG = True
		updated = open("rc3_updated.txt",'a') 
		updated.write("ra       dec         new_ra      new_dec         radius \n")
		for obj in self.allObj:
			print("Working on PGC{}, at({} , {})".format(str(obj.pgc), str(obj.rc3_ra),str(obj.rc3_dec)))
			print str(obj.rc3_radius)
			try:
				rfits=obj.mosaic_band(survey.best_band,obj.rc3_ra,obj.rc3_dec,3*obj.rc3_radius,obj.rc3_radius,obj.pgc,survey)
				if(rfits!=-1): #Special value for outside footprint or error, no rfits produced
					obj.source_info(rfits,survey)
			except(AssertionError):
				print("Something went wrong in mosaicing PGC {}".format(str(obj.pgc)))
				if (not (os.path.exists("rc3Catalog.py"))):
					# if we are not in the outer directory where rc3Catalog.py is located at 
					# then we are stuck inside some sort of position directory.
					# Must get out to prevent spiraling recursion.
					print (os.getcwd())
					print ("Get out of cwd")
					os.chdir("..")
				print (os.getcwd())
				mosaicAll_error=open("mosaicAll_error","a")
				mosaicAll_error.write("{}       {}        {}        {} \n".format(str(obj.rc3_ra),str(obj.rc3_dec),str(obj.rc3_radius),str(obj.pgc)))
				pass

	def __str__(self):
		x = "["
		for i in self.allObj:
			x=x+","+ str(i)
		x=x+"]"
		return x
