from sdss import SDSS
from rc3 import RC3
pgc3377 = RC3(14.1779166667,-9.91416666667,0.0527046277749,3377)
sdss = SDSS()
radius = 0.0527046277749
rfits = pgc3377.mosaic_band('r',14.1779166667,-9.91416666667,3*radius,radius,3377,sdss)
rfits = 'SDSS_r_3377.fits'
update = pgc3377.source_info(rfits,sdss)
pgc3377.mosaic_all_bands(update[0],update[1],update[2],update[3],update[4],sdss)