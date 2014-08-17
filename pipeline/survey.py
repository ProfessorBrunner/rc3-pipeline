from dssServer import DSSServer
from gator import Gator
from skyserver import SkyServer
from server import Server
class Survey(object):
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

    def _initServer(self):
        #Type Dispatching
        if (self.name =='2MASS' or self.name == 'WISE' or self.name == 'IRAS'):
            return Gator()
        # <Can add other surveys here> such as:
        # elif (self.name =='GALEX'):
        #     return MAST()
        #     pass
        elif (self.name == 'DSS'):
            return DSSServer()
        elif (self.name=='SDSS'):
            return SkyServer()
        else: #Generic
            raise TypeError("Unsupported survey type")
        
