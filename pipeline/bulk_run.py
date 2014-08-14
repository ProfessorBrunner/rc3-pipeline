from rc3Catalog import RC3Catalog 
from sdss import SDSS
from rc3 import RC3
rc3cat = RC3Catalog()
sloan = SDSS()
rc3cat.mosaicAll(sloan)
