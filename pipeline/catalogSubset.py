import os
from rc3 import RC3
from rc3Catalog import RC3Catalog
subset = RC3Catalog()
subsetlst= subset.initSubset("catalogSubset.txt")
subset.allObj = subsetlst
from sdss import SDSS
sdss = SDSS()
subset.mosaicAll(sdss)
