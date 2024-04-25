import mysql.connector
from mysql.connector import cursor
import config as cfg

import requests
import json
import sys
        

class AdminDao:
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
     
def create(self, admin):
    cursor = self.db.cursor()
    sql = "INSERT INTO admin (id, email, password) VALUES (%s, %s, %s,)"
    values = (admin['id'], admin['email'], admin['password'])
    cursor.execute(sql, values)
    self.db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid
print("user has been inserted to the database")

def getAll(self):
    cursor = self.db.cursor()
    sql = "select * from admin"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return [self.convertToDictionary(result) for result in results]
print('running get all statement')


def findById(self, id):
    cursor = self.db.cursor()
    sql = "SELECT * FROM admin WHERE id = %s"
    values = (id)
    cursor.execute(sql, values)
    result = cursor.fetchone()  
    cursor.close()
    return self.convertToDictionary(result) if result else None
print("running statement from the database")


def update(self, id, admin):
    cursor = self.db.cursor()
    sql = "UPDATE admin SET  email = %s, password = %s WHERE id = %s"
    values = (admin['email'], admin['password'])
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    
def delete(self, id):
    cursor = self.db.customer()
    sql = "delete from admin where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    print("deleting from the database")
    
def convertToDictionary(self, result):
        # Helper function to convert database row to a dictionary
        colnames = ['id'],['email'],['password']
        user = {colname: result[idx] for idx, colname in enumerate(colnames)}
        return user

AdminDao = AdminDao