# Survey Class for the Digitized Sky Survey
from survey import *
class DSS(Survey):
    def __init__(self):
        self.name = 'DSS'
        self.bands=['1b','1r','2b','2r','2ir']
        self.color_bands=['2b','2r','2ir']
        self.best_band ='2r'
        self.data_server = Survey._initServer(self)
        # 1.0 arcsec/pix for POSS-I survey
        # 1.7 arcsec/pix for POSS-II survey  
        # Since we are doing astrometry on 2r (best_band), we use PIXEL_SCALE=1.7
        self.pixel_scale = 1.7
        # Mosaic Program Settings
        self.sextractor_params= " -PIXEL_SCALE {}".format(self.pixel_scale)
        # Changes to STIFF param tested in 07-31-2014 Notebook 
        self.stiff_param_low = " -COPY_HEADER Y -MAX_TYPE QUANTILE   -MAX_LEVEL 0.99 -COLOUR_SAT  1 -MIN_TYPE QUANTILE -MIN_LEVEL 0.001  -GAMMA_FAC 1 "
        self.stiff_param_best = " -COPY_HEADER Y -MAX_TYPE QUANTILE  -MAX_LEVEL 1 -COLOUR_SAT  1 -MIN_TYPE QUANTILE -MIN_LEVEL 0.7 -GAMMA_FAC 0.9" 
