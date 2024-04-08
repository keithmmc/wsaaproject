import mysql.connector 

connection = mysql.connector.connect(
    host = "localhost", 
    user = "root", 
    password = "pass"
)


mycursor = connection.cursor()
mycursor.execute("CREATE database flaskdb")
mycursor.close()
connection.close()


