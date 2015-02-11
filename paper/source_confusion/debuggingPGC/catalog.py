from abc import ABCMeta , abstractmethod

class Catalog(object):
	'''
	Class for Catalog objects
	'''
	__metaclass__= ABCMeta

	def __init__(self):
		self.name= 'Catalog'
		self.frame= 'fk5'
		self.equinox = 'J2000'
		self.allObj=_initAllObj()

	@abstractmethod
	def _initAllObj(self):
		'''
		Create a list of all objects inside the catalog
		'''
		raise NotImplementedError()



	@abstractmethod
	def mosaicAll(self,survey):
		'''
		survey : Survey object
		Produce all band FITS files and color mosaic for every objects inside the Catalog that lies within the footprint of the given survey
		'''          
		raise NotImplementedError()

	def printAll(self):
		pass