# __Survey__ implements the abstract methods in the __Data__  class. It can also call on  appropriate methods from Gator or MAST data class. For the program to work properly, survey must have capabilities which is covered by the folowing method.
# import Gator,MAST
from dssServer import DSSServer
from gator import Gator
from skyserver import SkyServer
from server import Server
class Survey(object):
    # def __init__(self,bands,color_bands,best_band,pixel_size,sextractor_params,montage_params,stiff_params):
    def __init__(self):
        self.name=name
        # Preset defaults for the specific survey
        self.bands = []
        self.color_bands= []
        self.best_band='@'
        self.pixel_size= -1
        self.data_server=self._initServer()
        # Mosaic Program Settings
        self.sextractor_params={} 
        self.montage_params={}
        self.stiff_params={}
    # def search(query,database):

    def _initServer(self):
        #Type Dispatching
        if (self.name =='2MASS' or self.name == 'WISE' or self.name == 'IRAS'):
            return Gator()
        elif (self.name =='GALEX'):
            #Not implemented yet
            # return MAST()
            pass
        elif (self.name == 'DSS'):
            return DSSServer()
        elif (self.name=='SDSS'):
            # print ("sdss server")
            # print (SkyServer())
            return SkyServer()
            # print (self.data_server)
        else: #Generic
            raise TypeError("Unsupported survey type")
        
