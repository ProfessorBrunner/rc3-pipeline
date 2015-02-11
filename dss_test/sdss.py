from survey import *
class SDSS(Survey):
    def __init__(self):
        self.name='SDSS'
        self.bands=['u','g','r','i','z']
        self.color_bands=['g','r','i']
        self.best_band='r'
        self.data_server=Survey._initServer(self)
        self.pixel_scale =  0.396 #(arcsec/pix)
        # Mosaic Program Settings
        self.sextractor_params= " -PIXEL_SCALE {}".format(self.pixel_scale)
        self.stiff_param_low = " -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 "
        self.stiff_param_best = " -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8" 


