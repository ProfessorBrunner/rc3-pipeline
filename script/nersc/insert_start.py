import sys
print sys.argv
n=int(sys.argv[1])
linenumber=int(sys.argv[2])
print n  
print linenumber
f = open("rc3_ra_dec_diameter_pgc.txt".format(n),'r')
contents = f.readlines()
contents.insert(linenumber, "@ \n")
contents = "".join(contents)
#print contents
f.close()
f = open("rc3_ra_dec_diameter_pgc.txt".format(n),'w')
f.write(contents)
f.close()
