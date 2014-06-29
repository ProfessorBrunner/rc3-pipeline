import sqlcl
import numpy as np
with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
    for line in f:
        ra = float(line.split()[0])
        dec = float(line.split()[1])
        radius = float(line.split()[2])/2. #radius = diameter/2'
        margin = 3*radius
        pgc=str(line.split()[3]).replace(' ', '')
        clean=True
        filename = "{},{}".format(str(ra),str(dec))
        other_rc3s = sqlcl.query("SELECT distinct rc3.ra, rc3.dec FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE po.ra between {0}-{1} and  {0}+{1} and po.dec between {2}-{3} and  {2}+{3}".format(str(ra),str(margin),str(dec),str(margin))).readlines()
        data =[]
        count =0
        for i in other_rc3s:
            if count>1:
                list =i.split(',')
                list[0] = float(list[0])
                list[1]= float(list[1][:-1])
                data.append(list)
            count += 1 
        print (data)
        if (len(data)>1 and len(data)%2==0):
            d2p= np.array(data[0])-np.array(data[1])
            print ("d2p: {}".format(d2p))
            # if negative then a is on the left of b
            # if positive then b is on the right of b
            # or something like that
            # then we do pairwise comparison to figure out their relative locations
        #Finding the difference between the 2 points
        # d2p = np.array()-np.array()



            # a = sqlcl.query("SELECT distinct rc3.ra ,rc3.dec, rc3.pgc FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE rc3.pgc={}".format(str(pgc_a))).readlines()
            # b = sqlcl.query("SELECT distinct rc3.ra ,rc3.dec, rc3.1 FROM PhotoObj as po JOIN RC3 as rc3 ON rc3.objid = po.objid  WHERE rc3.pgc={}".format(str(pgc_b))).readlines()
            # print (a)
            # print (b)