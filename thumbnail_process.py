#Keep only BEST images abd convert all TIFF color images to .gif
import os 
import glob
os.chdir("Mosaic")
bests = glob.glob("*_BEST.tiff")
for i in bests:
	print (i)
	os.system("gm convert -resize 128x128\! {} {}.gif".format(i,i[:-5]))
os.system("rm *.tiff")
os.chdir("..")
os.rename("Mosaic", "img")