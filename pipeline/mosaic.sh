mImgtbl projdir images.tbl
mOverlaps images.tbl diffs.tbl
mDiffExec -p projdir diffs.tbl template.hdr diffdir
mFitExec diffs.tbl fits.tbl diffdir
mBgModel images.tbl fits.tbl corrections.tbl
mBgExec -p projdir images.tbl corrections.tbl corrdir
mAdd -p corrdir images.tbl template.hdr mosaic.fits
mJPEG -gray mosaic.fits 0s max gaussian-log -out mosaic.jpg