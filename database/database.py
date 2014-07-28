import sqlite3
def create_table(db_name,table_name,sql): #sql statement that you want to take
    with sqlite3.connect(db_name) as db: #open db and do stuff within function. If crashes then connection automatically closed.
        cursor = db.cursor() #give latest info about navigate around database
        cursor.execute("select name from sqlite_master where name =?",(table_name,)) #check if the table already exist 
        result = fetchall() #get result from query
        keep_table = True
        if len(result)==1:
        	response = input("The table {0} already exist , do you wish to recreate it ")
        	if response == 'y':
        		keep_table=False
        		print ("The {0} table will be recreated - all existing data will be lost ".format(table_name))
        		cursor.execute("drop table if exist{0}".format(table_name))
        		db.commit()
        	else : 
        		print ("The existing table was kept")
        else : 
        	keep_table = False
        if not keep_table:        	
	        cursor.execute(sql) #execute query
	        db.commit() #saved
        
if __name__=="main":
    db_name="coffee_shop.db"
    #create table statement in SQL, ProductID act as primary attribute key
    sql = """CREATE TABLE Product
            (ProductID integer,
            Name text,
            Price real,
            primary key(ProductID)) 
            """
    create_table(db_name,"Product",sql)