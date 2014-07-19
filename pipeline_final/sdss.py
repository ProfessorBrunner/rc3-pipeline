from survey import *
class SDSS(Survey):
    def __init__(self):
        self.name='SDSS'
        self.bands=['u','g','r','i','z']
        self.color_bands=['g','r','i']
        self.best_band='r'
        self.pixel_size=0.396
        self.data_server=Survey._initServer(self)
        # Mosaic Program Settings
        self.sextractor_params={} 
        self.montage_params={}
        self.stiff_params={}
        # super(SDSS,self).__init__(name,bands,color_bands,best_band,pixel_size,sextractor_params,montage_params,stiff_params)


