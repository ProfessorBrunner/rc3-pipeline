#Installing LibTIFF
wget http://download.osgeo.org/libtiff/tiff-3.9.5.tar.gz
gunzip tiff-3.9.5.tar.gz
tar -xvf  tiff-3.9.5.tar
cd tiff-3.9.5
./configure
make
sudo make install
#Installing LibJPEG
wget http://sourceforge.net/projects/libjpeg/files/libjpeg/6b/jpegsrc.v6b.tar.gz
gunzip jpegsrc.v6b.tar.gz 
tar -xvf jpegsrc.v6b.tar 
cd jpeg-6b/
make
make test
make -n install
sudo make install
#Installing zlib
wget http://zlib.net/zlib-1.2.8.tar.gz
gunzip zlib-1.2.8.tar.gz 
tar -xvf zlib-1.2.8.tar
cd zlib-1.2.8
./configure
make
sudo make install
#Installing STIFF
wget http://www.astromatic.net/download/stiff/stiff-2.4.0.tar.gz
gunzip stiff-2.4.0.tar.gz
tar -xvf stiff-2.4.0.tar
cd stiff-2.4.0
./configure
make
make install
sudo make install