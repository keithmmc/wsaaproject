import mysql.connector
from mysql.connector import cursor
import config as cfg

import requests
import json
import sys
        

class DataDAO:
    def initConnectToDB(self):
        db = mysql.connecter.connect(
        host = cfg.mysql['host'],
        user = cfg.mysql['user'],
        password = cfg.mysql['pass'], 
        database=cfg.mysql['keithsshop']
     )
        return db 
   
def __init__(self):
     db = self.initConnectToDB()
     db.close()
     print('you are connected to the database') 
     
def create(self, customer):
    cursor = self.db.cursor()
    sql = "INSERT INTO customer (cid, email, username, age, password) VALUES (%s, %s, %s, %s, %s)"
    values = (customer['cid'], customer['email'], customer['username'], customer['age'], customer['password'])
    cursor.execute(sql, values)
    self.db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid
print("user has been inserted to the database")

def getAll(self):
    cursor = self.db.cursor()
    sql = "select * from customer"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return [self.convertToDictionary(result) for result in results]
print('running get all statement')


def findById(self, cid):
    cursor = self.db.cursor()
    sql = "SELECT * FROM customer WHERE cid = %s"
    values = (cid)
    cursor.execute(sql, values)
    result = cursor.fetchone()  
    cursor.close()
    return self.convertToDictionary(result) if result else None
print("running statement from the database")


def update(self, cid, customer):
    cursor = self.db.cursor()
    sql = "UPDATE customer SET username = %s, email = %s, age = %s, password = %s WHERE cid = %s"
    values = (customer['username'], customer['email'], customer['age'], customer['password'])
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    
def delete(self, cid):
    cursor = self.db.customer()
    sql = "delete from customer where cid = %s"
    values = (cid,)
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    print("deleting from the database")
    
def convertToDictionary(self, result):
        # Helper function to convert database row to a dictionary
        colnames = ['cid'],['username'],['email'],['age'],['password']
        user = {colname: result[idx] for idx, colname in enumerate(colnames)}
        return user

DataDAO = DataDAO 

    
    

