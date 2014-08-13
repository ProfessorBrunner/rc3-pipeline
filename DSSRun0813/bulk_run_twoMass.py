from rc3Catalog import RC3Catalog 
# from sdss import SDSS
from twoMass import TwoMass
from rc3 import RC3
rc3cat = RC3Catalog()
tm = TwoMass()
rc3cat.mosaicAll(tm)