# Data from Vizier
  #  1-  2  I2    h       RAh      *Right Ascension B2000 (hours)
  #  3-  4  I2    min     RAm      *Right Ascension B2000 (minutes)
  #  5-  8  F4.1  s       RAs      *Right Ascension B2000 (sec. or min.)
  #     10  A1    ---     DE-       [-+] Sign of declination
  # 11- 12  I2    deg     DEd      *Declination B2000 (degrees)
  # 13- 14  I2    arcmin  DEm      *Declination B2000 (minutes)
  # 15- 16  I2    arcsec  DEs      *? Declination B2000 (seconds)
  # 18- 19  I2    h       RA1950h   Right Ascension 1950 (hours)
  # 20- 21  I2    min     RA1950m   Right Ascension 1950 (minutes)
  # 22- 25  F4.1  s       RA1950s  *Right Ascension 1950 (sec. or min.)
  #     27  A1    ---     DE1950-   [-+] Sign of declination 1950
  # 28- 29  I2    deg     DE1950d   Declination 1950 (degrees)
  # 30- 31  I2    arcmin  DE1950m   Declination 1950 (minutes)
  # 32- 33  I2    arcsec  DE1950s  *? Declination 1950 (seconds)


#Run in Python2 
output =  open("rc3_parsed.txt", "w")
inaccurate_count = 0
accurate_count = 0
total= 0
for line in file('rc3.txt'):
    s = line[4:8]
    s= s.split('.')
    # print (s)    
    if (s[1]==' '):
        # print ("inaccurate")
        inaccurate_count+=1
    else:
        # print ("accurate")
        accurate_count+=1
    total+=1

print ("inaccurate_count : {}".format(inaccurate_count))
print ("accurate_count : {}".format(accurate_count))
print ("total : {}".format(total))


        

    # if (s)
#     output.write(str(s)+ "    \n ")
# output.close()
