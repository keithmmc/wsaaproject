
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

# Create the cars Table
cursor.execute("CREATE TABLE band(\
    id int NOT NULL AUTO_INCREMENT,\
    name varchar(250),\
    genre varchar(250),\
    info varchar(250),\
    PRIMARY KEY(id)\
    )") 

# Create the Customer Table
cursor.execute("CREATE TABLE customer(\
    cid int NOT NULL AUTO_INCREMENT,\
    email varchar(250),\
    name varchar(250),\
    age int,\
    password varchar(250),\
    PRIMARY KEY(cid)\
    )") 

cursor.execute("CREATE TABLE product(\
    pid int NOT NULL AUTO_INCREMENT,\
    amount int,\
    name varchar(250),\
    price int,\
    info varchar(250),\
    PRIMARY KEY(pid)\
    )") 


db.commit()
print("connected to db")
