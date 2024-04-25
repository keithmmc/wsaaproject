
import pymysql
from mysql.connector import cursor

# Connect to MySQL
db = pymysql.connect(
    host="localhost", 
    user = "root", 
    password = "pass"
    )

cursor = db.cursor() 
cursor.execute("DROP DATABASE IF EXISTS keithsstore")
cursor.execute("CREATE DATABASE keithsstore")
cursor.execute("USE keithsstore")

 

# Create the Customer Table
cursor.execute("CREATE TABLE customer(\
    cid int NOT NULL AUTO_INCREMENT,\
    email varchar(250),\
    username varchar(250),\
    age int,\
    password varchar(250),\
    PRIMARY KEY(cid)\
    )") 


cursor.execute("CREATE TABLE product(\
    id int NOT NULL AUTO_INCREMENT,\
    amount int,\
    name varchar(250),\
    price int,\
    info varchar(250),\
    PRIMARY KEY(id)\
    )") 

cursor.execute("CREATE TABLE orders(\
    id int NOT NULL AUTO_INCREMENT,\
    email varchar(250),\
    amount int,\
    eircode varchar(10),\
    PRIMARY KEY(id)\
    )") 

cursor.execute("CREATE TABLE admin(\
   id int NOT NULL AUTO_INCREMENT,\
    email varchar(250),\
    password varchar(20),\
    primary key(id)\
    )")

cursor.execute("CREATE TABLE contact(\
    fname varchar(250),\
    lname varchar(250),\
    email varchar(250)\
    )") 


db.commit()
print("connected to db")
