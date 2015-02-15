#Run in Python2 
output =  open("rc3_ra_dec_only(Final).txt", "w")
#output.write("ra          |")
#output.write("dec          |")
#output.write("radius          \n")
for line in file('rc3.txt'):
    x = float(line[0:2])
    y = float(line[2:4])
    z = float(line[4:8])
    sign = line[9]
    decval = float(line[10:12]) 
    m = float(line[12:14])
    if line[14] != ' ' and line[15] != ' ':        
        n = float(line[14:16])
    if line[172]!= ' ' : #everything except blank line should have decimal point
        rad = 10**(float(line[171:175]))
        ra = 15.*x + (y/4.) + (z/240.) #units of time 0-24 hr,=>degrees, every hour earth spins 15 deg  (4, 240 comes from expaned form from 3600)
        diameter = rad*0.00166666667 # arcminute to degrees
        #print ('diameter: '+str(diameter) + "\n")
    dec = decval + (m/60.) + (n/3600.)
    if sign == '-':
       dec = -1*dec 
    output.write(str(ra)+ "     ")
    #output.write(str(dec)+ "     ")
    #output.write(str(diameter)+"\n")
    output.write(str(dec)+ "\n")
    #output.write(str(diameter)+"\n")
output.close()
