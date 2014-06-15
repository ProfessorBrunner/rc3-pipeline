import sqlite3
conn = sqlite3.connect("rc3.db")
c = conn.cursor()
def tableCreate():
	#this can only be done once
	c.execute("CREATE TABLE rc3 (ID INT , PGC_number TEXT,ra REAL, dec REAL,radius REAL, PRIMARY KEY(ID))")#, in_SDSS_footprint BOOLEAN ") # create table and specify column, primary key is auto incremnting ID numbe

def dataEntry():
	# for sdss in file('rc3_galaxies_outside_SDSS_footprint'):
	n=0
	with open("rc3_ra_dec_diameter_pgc.txt",'r') as f:
		for line in f:
			ra = float(line.split()[0])
			dec = float(line.split()[1])
			radius = float(line.split()[2])/2.
			pgc=str(line.split()[3]).replace(' ', '')
			print (ra,dec,radius,pgc)
			c.execute("INSERT INTO rc3 VALUES({},{},{},{},{})".format(n,pgc,ra,dec,radius))#,in_SDSS_footprint)")
			n+=1
			conn.commit()
if __name__ == "__main__":
	print ("Create TABLE")
	tableCreate()
	print ("Enter Data") 
	dataEntry()
