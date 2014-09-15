import os 
with open("allRC3pgc.txt",'r') as f:
	for line in f:
		pgc = str(line)[0]
		query  ="http://www.nsatlas.org/getAtlas.html?search=name&name=PGC{}&radius=10.0&submit_form=Submit".format(pgc)
		print query
		os.system("wget -r  {}".format(query))
		# os.system("rm temp.xml")