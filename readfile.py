counter = 0

ralist = []
declist = []
radiuslist = []

for line in file('rc3.txt'):
       
    counter = counter + 1
    if counter > 15:
        break
        
    if counter != 5 and counter != 6 and counter != 7 and counter != 11:
        
        x = float(line[0:2])
        y = float(line[2:4])
        z = float(line[4:8])
         
        sign = line[9]
        decval = float(line[10:12]) 
        m = float(line[12:14])
        
##     #   if line[14] != ' ' and line[15] != ' ':        
        n = float(line[14:16])
        
        # testval = float(line[171:175])
        rad = 10**(float(line[171:175]))
        radius = rad/10
        
        ra = 15*x + (y/4) + (z/240) 
##      #  if line[14] != ' ' and line[15] != ' ':
        dec = decval + (m/60) + (n/3600)   
##      else:
#        dec = decval + (m/60)
        
        if sign == '-':
           dec = -1*dec 
              
        ralist.append(ra)
        declist.append(dec)
        radiuslist.append(radius)
        
       # print ra, dec
       # print radius 

print ralist
print declist
print radiuslist        