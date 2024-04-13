import mysql.connector
from mysql.connector import cursor
import config as cfg

import requests
import json
import sys

class OrderDAO:
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
     
def create(self, order):
    cursor = self.db.cursor()
    sql = "INSERT INTO order (username, amount, price, shipping eircode) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (order['username'], order['amount'], order['price'], order['shipping'], order['eircode'])
    cursor.execute(sql, values)
    self.db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid
print("order has been inserted to the database")

def getAll(self):
    cursor = self.db.cursor()
    sql = "select * from order"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return [self.convertToDictionary(result) for result in results]
print('running get all statement')


def findById(self, id):
    cursor = self.db.cursor()
    sql = "SELECT * FROM order WHERE id = %s"
    values = (id)
    cursor.execute(sql, values)
    result = cursor.fetchone()  
    cursor.close()
    return self.convertToDictionary(result) if result else None
print("running statement from the database")


def update(self, id, order):
    cursor = self.db.cursor()
    sql = "UPDATE order SET username = %s, amount = %s, price = %s, shipping = %s,  eircode = %s WHERE id = %s"
    values = (order['username'], order['amount'], order['price'], order['shipping'], order['eircode'])
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    
def delete(self, id):
    cursor = self.db.customer()
    sql = "delete from order where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()
    print("deleting from the database")
    
def convertToDictionary(self, result):
        # Helper function to convert database row to a dictionary
        colnames = ['username'] ['amount'] ['price'] ['shipping'] ['eircode']
        user = {colname: result[idx] for idx, colname in enumerate(colnames)}
        return user

OrderDAO = OrderDAO
    
