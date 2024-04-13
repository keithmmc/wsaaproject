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
        database=cfg.mysql['flaskdb']
     )
        return db 
   
def __init__(self):
     db = self.initConnectToDB()
     db.close()
     print('you are connected to the database') 
     
def create(self, user):
    cursor = self.db.cursor()
    sql = "INSERT INTO user (username, email, password, phone, eircode) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user['username'], user['email'], user['password'], user['phone'], user['eircode'])
    cursor.execute(sql, values)
    self.db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid
print("user has been inserted to the database")

def getAll(self):
    cursor = self.db.cursor()
    sql = "select * from user"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return [self.convertToDictionary(result) for result in results]
print('running get all statement')


def findById(self, id):
    cursor = self.db.cursor()
    sql = "SELECT * FROM user WHERE id = %s"
    values = (id)
    cursor.execute(sql, values)
    result = cursor.fetchone()  
    cursor.close()
    return self.convertToDictionary(result) if result else None
print("running statement from the database")


def update(self, id, user):
    cursor = self.db.cursor()
    sql = "UPDATE user SET username = %s, email = %s, last_name = %s, password = %s, phone = %s, eircode = %s WHERE id = %s"
    values = (user['username'], user['email'], user['password'], user['phone'], user['eircode'])
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    
def delete(self, id):
    cursor = self.db.customer()
    sql = "delete from customer where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    print("deleting from the database")
    
def convertToDictionary(self, result):
        # Helper function to convert database row to a dictionary
        colnames = ['username'] ['email'] ['password'] ['phone'] ['eircode']
        user = {colname: result[idx] for idx, colname in enumerate(colnames)}
        return user

DataDAO = DataDAO 

    
    

