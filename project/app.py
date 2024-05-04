from flask import Flask, url_for, request, redirect, abort, jsonify,render_template, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import mysql.connector
import json
from shop_dao import shop_dao


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')



@app.route('/shirts', methods=['GET'])
def getAll():
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute('SELECT * FROM productdata')
    shirts = mycursor.fetchall()
    shop_dao.close_all(mycursor, connection)

    # Create a list of dictionaries for each shoe
    shirt_list = [{'id': shirt[0], 'Product': shirt[1], 'Model': shirt[2], 'Price': shirt[3]} for shirt in shirts]
    return jsonify({'shirts': shirt_list})

# Find by Id
@app.route('/shirts/<int:id>')
def findById(id):
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    shirt = mycursor.fetchone()
    shop_dao.close_all(mycursor, connection)
    if not shirt:
        return jsonify({}), 204
    return jsonify({'shirt': {'id': shirt[0], 'Product': shirt[1], 'Model': shirt[2], 'Price': shirt[3]}})

# Create
# curl -X POST -H "Content-Type: application/json" -d "{\"Product\": \"New Product\", \"Model\": \"New Model\", \"Price\": 123}" http://127.0.0.1:5000/shoes
@app.route('/shirts', methods=['POST'])
def create():
    mycursor, connection = shop_dao.get_cursor()

    if not request.json:
        abort(400)

    new_shirt = {
        'Product': request.json['Product'],
        'Model': request.json['Model'],
        'Price': request.json['Price']
    }

    sql = 'INSERT INTO productdata (Product, Model, Price) VALUES (%s, %s, %s)'
    values = (new_shirt['Product'], new_shirt['Model'], new_shirt['Price'])

    mycursor.execute(sql, values)
    connection.commit()

    new_shirt['id'] = mycursor.lastrowid
    shop_dao.close_all(mycursor, connection)
    return jsonify({'shirt': new_shirt}), 201

# Update
# curl -X PUT -H "Content-Type: application/json" -d "{\"Product\": \"Updated Product\", \"Model\": \"Updated Model\", \"Price\": 200}" http://127.0.0.1:5000/shoes/6
@app.route('/shirts/<int:id>', methods=['PUT'])
def update(id):
    mycursor, connection = shop_dao.get_cursor()

    # Check if the product with the given ID exists
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    current_shirt = list(mycursor.fetchone())

    if not current_shirt:
        return jsonify({}), 404

    if 'Product' in request.json:
        current_shirt[1] = request.json['Product']
    if 'Model' in request.json:
        current_shirt[2] = request.json['Model']
    if 'Price' in request.json:
        current_shirt[3] = request.json['Price']

    sql = 'UPDATE productdata SET Product=%s, Model=%s, Price=%s WHERE id=%s'
    values = (current_shirt[1], current_shirt[2], current_shirt[3], id)

    mycursor.execute(sql, values)
    connection.commit()

    shop_dao.close_all(mycursor, connection)
    return jsonify({'shirt': {'id': current_shirt[0], 'Product': current_shirt[1], 'Model': current_shirt[2], 'Price': current_shirt[3]}})

# Delete
# curl -X DELETE http://127.0.0.1:5000/shoes/7
@app.route('/shirts/<int:id>', methods=['DELETE'])
def delete(id):
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    deleted_shirt = mycursor.fetchone()

    if not deleted_shirt:
        return jsonify({}), 404

    sql = 'DELETE FROM productdata WHERE id=%s'
    values = (id,)
    mycursor.execute(sql, values)
    connection.commit()
    
    shop_dao.close_all(mycursor, connection)
    return jsonify({"done":True})

# New route for creating an order
@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.json

    # Retrieve order details
    product_id = data.get('productId')
    product_name = data.get('productName')
    quantity = data.get('quantity')
    total_price = data.get('totalPrice')

    # Add order to the orderdata database
    order_data = shop_dao.create_order(product_id, quantity, total_price)

    return jsonify({'order': order_data}), 201

def get_products():
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute('SELECT * FROM productdata')
    products = mycursor.fetchall()
    shop_dao.close_all(mycursor, connection)

    # Create a list of dictionaries for each product
    products_list = [{'id': product[0], 'Product': product[1], 'Model': product[2], 'Price': product[3]} for product in products]
    return products_list

app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Hard-coded user for demonstration purposes
users = {'1': {'username': 'admin', 'password': 'pass'}}

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello!  <a href='/logout'>Logout</a>"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get('1')  # Hard-coded user for demonstration purposes

        if user and user['password'] == password:
            user_obj = User('1')
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('product_list'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route to render the product list page
@app.route('/shop')
def product_list():
    products = get_products()
    return render_template('shop.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)

