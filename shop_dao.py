import mysql.connector
import json

class ShopDAO:
    def __init__(self, config_path='config.json'):
        self.config = self.read_config(config_path)
    
    def read_config(self, config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config['Database']

    def get_cursor(self):
        connection = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )
        mycursor = connection.cursor()
        return mycursor, connection
    
    def close_all(self, mycursor, connection):
        connection.close()
        mycursor.close()

    def create_order(self, product_id, quantity, total_price):
        mycursor, connection = self.get_cursor()

        # Insert a new order into the 'orderdata' table
        order_sql = '''
            INSERT INTO orderdata (ProductID, Quantity, TotalPrice) 
            VALUES (%s, %s, %s)
        '''
        values = (product_id, quantity, total_price)

        mycursor.execute(order_sql, values)
        connection.commit()

        # Close the cursor and connection
        self.close_all(mycursor, connection)

shop_dao = ShopDAO()
mycursor, connection = shop_dao.get_cursor()

# First database table 'productdata'
sql= '''
    CREATE TABLE IF NOT EXISTS productdata (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Product VARCHAR(300),
        Model VARCHAR(200),
        Price INT
    )
'''
mycursor.execute(sql)

# Second database table 'orderdata'
order_sql = '''
    CREATE TABLE IF NOT EXISTS orderdata (
        OrderID INT AUTO_INCREMENT PRIMARY KEY,
        ProductID INT,
        Quantity INT,
        TotalPrice INT,
        FOREIGN KEY (ProductID) REFERENCES productdata(ID)
    )
'''
# Execute the SQL statement
mycursor.execute(order_sql)
connection.commit()
shop_dao.close_all(mycursor, connection)