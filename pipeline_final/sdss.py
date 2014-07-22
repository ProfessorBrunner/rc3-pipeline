from survey import *
class SDSS(Survey):
    def __init__(self):
        self.name='SDSS'
        self.bands=['u','g','r','i','z']
        self.color_bands=['g','r','i']
        self.best_band='r'
        # self.pixel_size=0.396
        self.data_server=Survey._initServer(self)
        # Mosaic Program Settings
        # self.sextractor_params={} 
        # self.montage_params={}
        # self.stiff_params={}
        self.stiff_param_low = " -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 "
        self.stiff_param_best = " -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8" 

        # super(SDSS,self).__init__(name,bands,color_bands,best_band,pixel_size,sextractor_params,montage_params,stiff_params)


