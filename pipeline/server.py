#Data object is an abstract class for accessing raw data from survey and feed it into program in the appropraite format.
'''
Instance Attributes:
    - str raw : unprocessed raw data in CSV or HTML format
    - str processed: processed data in desirable format (list?, or just text file and do readline())
    - Useful quantities parse columns into list and store as attributes(?) 
'''
# import survey
# import mast
# import gator
from abc import ABCMeta , abstractmethod

class Server(object):
    __metaclass__= ABCMeta
	#Optional 
    # def process():
    #     #Processing data
    #     '''
    #     Implemented by Catalog 
    #     '''
    #     #return null
    def __init__(self):
        self.name = 'Server'
    
    @abstractmethod
    def query (self,query): 
        '''
        Query the server database
        '''
        raise NotImplementedError()

    @abstractmethod
    def getData(self,*args):
        '''
        Downloads imaging data from server
        '''
        raise NotImplementedError()
    
    def __str__(self):
        return "The {} Server Object".format(self.name)
