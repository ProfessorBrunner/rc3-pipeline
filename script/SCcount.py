import numpy as np
ra= []
dec = []
radius=[]
pgc=[]
rc3= {}
with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
	for line in f:
		a = str(line)[0]
		if a[0] =="@": 
			start=True
			continue
		if (start):
			rai = float(line.split()[0])
			deci=float(line.split()[1])
			radi=float(line.split()[2])/2.
			ra.append(rai)
			dec.append(deci)
			radius.append(radi)
			pgci=int(str(line.split()[3]).replace(' ', ''))
			pgc.append(pgci)
			rc3[pgci]=[rai,deci,radi]
sc=set()
for i in ra:
	deci= dec[ra.index(i)]
	pi = pgc[ra.index(i)]
	print (pi)
	for j in ra:
		d = dec[ra.index(j)]
		r = radius[ra.index(j)]
		p = pgc[ra.index(j)]
		if ((i+3*r> j and j> i-3*r) and (deci+3*r>d and d>deci-3*r) and pi!=p):
			print p
			print ("Source confusion")
			sc = sc.union([p])
		
		# else:
		# 	print ("--")
			# ra=[]
			# dec=[]
			# for i in rc3.values():
			# 	ra.append(i[0])
			# 	dec.append(i[1])
