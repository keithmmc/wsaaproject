import mysql.connector
from mysql.connector import cursor
import config as cfg

import requests
import json
import sys
        

class ProductDAO:
    def initConnectToDB(self):
        db = mysql.connecter.connect(
        host = cfg.mysql['host'],
        user = cfg.mysql['user'],
        password = cfg.mysql['pass']
     )
        return db 
   
def __init__(self):
     db = self.initConnectToDB()
     db.close()
     print('you are connected to the database') 
     
def create(self, product):
    cursor = self.db.cursor()
    sql = self.db.cursor()
    sql = "INSERT INTO product (id, name, price, description) VALUES (%s, %s, %s, %s)"
    values = (product['id'], product['Name'], product['Price'], product['description'])
    cursor.execute(sql, values)
    self.db.commit()  
    lastrowid = cursor.lastrowid  
    cursor.close()
    return lastrowid

def get_all(self):
    cursor = self.db.cursor()
    sql = "SELECT * FROM product"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return [self.convertToDictionary(result) for result in results]

def findByID(self, id):
    cursor = self.db.cursor()
    sql = "SELECT * FROM product WHERE id = %s"
    values = (id,)
    
    cursor.execute(sql.values)
    result = cursor.fetchall()
    cursor.close()
    return self.convertToDictionary(result) if result else None

def update(self, id, customer):
    cursor = self.db.cursor()
    sql = "UPDATE product SET name = %s, price = %s,  description = %s WHERE id = %s"
    values = (customer['name'], customer['price'], customer['description'], id)
    cursor.execute(sql, values)
    self.db.commit()  
    cursor.close()

def delete(self, id):
    cursor = self.db.cursor()
    sql = "DELETE FROM product WHERE id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit() 
    cursor.close()
    
def convertToDictionary(self, result):
        # Helper function to convert database row to a dictionary
        colnames = ['id', 'name', 'price', 'description']
        customer = {colname: result[idx] for idx, colname in enumerate(colnames)}
        return customer

# Instantiate the CustomerDAO to be used elsewhere
ProductDao = ProductDAO()

     
