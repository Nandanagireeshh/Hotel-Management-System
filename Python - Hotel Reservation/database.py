import mysql.connector
password=""
database="my_hotel"
def select(q):
	cnx=mysql.connector.connect(user="root",password=password,host="localhost", database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	result=cur.fetchall()
	cur.close()
	cnx.close()
	return result


def update(q):
	cnx=mysql.connector.connect(user="root",password=password,host="localhost", database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.rowcount
	cur.close()
	cnx.close()
	return result


def updated(q, params):
	# Establish the connection
	cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
	cur = cnx.cursor(dictionary=True)

	# Execute the query with parameters
	cur.execute(q, params)  # Pass parameters as a tuple
	cnx.commit()  # Commit the changes

	# Get the number of affected rows
	result = cur.rowcount

	# Close the cursor and connection
	cur.close()
	cnx.close()

	# Return the number of affected rows
	return result


def delete(q):
	cnx=mysql.connector.connect(user="root",password=password,host="localhost", database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.rowcount
	cur.close()
	cnx.close()
def insert(q):
	cnx=mysql.connector.connect(user="root",password=password,host="localhost", database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.lastrowid
	cur.close()
	cnx.close()
	return result
def insert(q):
	cnx=mysql.connector.connect(user="root",password=password,host="localhost", database=database)
	cur=cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result=cur.lastrowid
	cur.close()
	cnx.close()
	return result


def inserted(q, params):
    cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
    cur = cnx.cursor()
    cur.execute(q, params)  # Use params here
    cnx.commit()
    result = cur.lastrowid
    cur.close()
    cnx.close()
    return result




