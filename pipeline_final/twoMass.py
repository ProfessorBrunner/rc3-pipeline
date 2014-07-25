# 2MASS Class can not be named starting with number 
from survey import Survey
class TwoMass(Survey):
    def __init__(self):
        self.name = '2MASS'
        self.bands=['j','h','k']
        self.color_bands=['j','h','k']
        self.best_band ='j' #not sure about this 
        # self.pixel_size = 2.0 
        self.data_server = Survey._initServer(self)
        # Mosaic Program Settings
        #would it be better OOP practice if I hard code this into dictionary ,or just make a new configuration file for each file and store the config filename here as string then pass it in.
        # self.sextractor_params={} 
        #self.montage_params={} # There is no survey depenedent params for montage, fot our purposes montage is purely used for mosaic geometry
        self.stiff_param_low = " -MAX_TYPE QUANTILE  -MAX_TYPE QUANTILE  -MAX_LEVEL 0.997 -COLOUR_SAT  7 -MIN_TYPE QUANTILE -MIN_LEVEL 1  -GAMMA_FAC 0.7 "
        self.stiff_param_best = " -MAX_TYPE QUANTILE  -MAX_LEVEL 0.99 -COLOUR_SAT  5  -MIN_TYPE QUANTILE -MIN_LEVEL 1 -GAMMA_FAC 0.8" 
        # super(SDSS,self).__init__(name,bands,color_bands,best_band,pixel_size,sextractor_params,montage_params,stiff_params)
