# Note: 2MASS Class can not be named starting with number 
from survey import Survey
class TwoMass(Survey):
    def __init__(self):
        self.name = '2MASS'
        self.bands=['j','h','k']
        self.color_bands=['j','h','k']
        self.best_band ='k' #see Fig 2 (Skrutskie et al. 2006)
        self.pixel_scale = 2.0
        self.data_server = Survey._initServer(self)
        # Mosaic Program Settings
        self.sextractor_params= " -PIXEL_SCALE {}".format(self.pixel_scale)
        self.stiff_param_low = " -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 "
        self.stiff_param_best = " -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8" 
