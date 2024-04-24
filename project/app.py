import os
from flask import Flask, url_for, request, redirect, abort, session, render_template, jsonify
from markupsafe import escape


app = Flask(__name__, static_url_path='', static_folder='static')
import stripe 
from DataDAO import DataDAO
from ProductDAO import ProductDAO
from OrderDao import OrderDao


@app.route('/')
def index():
     ##'username' in session:
        ##return 'Logged in as %s' % escape(session['username']) +\
        ##'<br><a href="'+'/home.html'+'">home</a>' +\
        ##'<br><a href="'+url_for('admin')+'">Admin</a>'
        ##return '<br><a href="'+'/home.html'+'">home</a>' 
    return app.send_static_file('home.html')
    
      


 

    
@app.route('/customer/', methods=['GET'])
def get_all():
    try:
        results = DataDAO.getAll()
        return jsonify(results)
    except Exception as e:
        print(f"Error getting products: {e}")
        abort(500)
        

@app.route('/customer/<int:cid>', methods=['PUT'])
def update(cid):
    foundUser = DataDAO.findByID(cid)
    if not foundUser:
        abort(404)

    if not request.json:
       abort(400, 'Missing JSON in request')

    try:
        DataDAO.update(cid, request.json)
        return jsonify(request.json)
    except Exception as e:
        print(f"Error updating user with id {cid}: {e}")
        abort(500)
        
@app.route('/customer/<int:id>', methods=['GET'])
def findById(cid):
    try:
        foundUser = DataDAO.findByID(cid)
        if foundUser:
            return jsonify(foundUser)
        else:
            abort(404)
    except Exception as e:
        print(f"Error finding user with id {cid}: {e}")
        abort(500)
        
@app.route('/customer/<int:id>', methods=['DELETE'])
def delete(cid):
    try:
        DataDAO.delete(cid)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting user with the id {cid}: {e}")
        abort(500)
        
@app.route('/product')
def getAll():
    results = ProductDAO.getAll()
    return jsonify(results)



@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        results = ProductDAO.getAll()
        return jsonify(results)
    elif request.method == 'POST':
        data = request.get_json()
        new_product_id = ProductDAO.create((product['amount'], product['name'], product['price'], product['info']))
        return jsonify({"id": new_product_id}), 201
    
#endpoint to retrieve products by ID
##@app.route('/product/<int:id>')
##def findById(id):
    ##foundProduct = ProductDAO.findByID(id)
    ##return jsonify(foundProduct)

         #Endpoint to delete a product by ID
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        # Call the delete method from the productDAO to delete the product
        ProductDAO.delete(id)
        return jsonify({"message": f"Product with ID {id} deleted successfully"})
    except Exception as e:
        # Handle any exceptions that may occur during deletion
        return jsonify({"error": f"Error deleting product with ID {id}: {str(e)}"}), 500
        
        # Endpoint to update a product by ID
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Call the update method from the productDAO to update the product
        ProductDAO.update((product['amount'], product['name'], product['price'], product['info'], id))
        
        return jsonify({"message": f"Product with ID {id} updated successfully"})
    except Exception as e:
        # Handle any exceptions that may occur during the update
        return jsonify({"error": f"Error updating product with ID {id}: {str(e)}"}), 500
    

@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")




@app.route('/orders', methods = ["GET"])
def get_order():
    if 'name' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'name' in session:
        return redirect(url_for('login'))
    try:
        results = OrderDao.getAll()
        return jsonify(results)
    
    except Exception as e:
        print(f"Error getting your orders: {e}")
        abort(500)
        


@app.route('/orders/<int:id>', methods=['DELETE'])
def deleteorder(id):
    try:
        OrderDao.delete(id)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting order with id {id}: {e}")
        abort(500)
        
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Call the update method from the productDAO to update the product
        OrderDao.update((orders['email'], orders['amount'], orders['eircode'], id))
        
        return jsonify({"message": f"Product with ID {id} updated successfully"})
    except Exception as e:
        # Handle any exceptions that may occur during the update
        return jsonify({"error": f"Error updating product with ID {id}: {str(e)}"}), 500
    
    
    
@app.route('/contact')
def contact():
     return app.send_static_file('contact.html')

    
@app.route('/history')
def history():
    if 'username' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    else:
        return redirect(url_for('login'))
    

    
    
@app.route('/checkout')
def checkout():
    if 'username' in session:
        return '<br><a href="'+'/basket.html'+'">basket</a>' 
    else:
        return redirect(url_for('login'))
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username in username and username[password][1] == password:
            session['username'] = username
            return redirect(url_for('admin.html'))
    return render_template("/login.html")
    
    
    
@app.route('/logout')
def logout():
    session.clear()
    return "you have not logged out"
    return redirect('/home.html')  

@app.route('/clear')
def clear():
    #session.clear()
    session.pop('counter',None)   

    return "done" 
   

@app.route('/process-payment', methods=['POST'])
def process_payment():
      payment_method_id = request.form.get('paymentMethodId')
      
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'euro',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
    )
    return {'id': session.id}

##@app.route('/process-payment', methods=['POST'])
##def process_payment():
    ##payment_method_id = request.form['paymentMethodId']
    ##amount = 1000  # Amount in cents

    ##try:
        # Create a PaymentIntent with the order amount and currency
        ##intent = stripe.PaymentIntent.create(
            ##amount=amount,
            ##currency='usd',
            ##payment_method=payment_method_id,
            ##confirm=True
        ##)
        ##return jsonify({'success': True})
    ##except stripe.error.StripeError as e:
       ## return jsonify({'error': str(e)}), 400
      



##@app.route('/failure')
##def failure():
    ##return "the payment failed please try again and make payment"
    ####return redirect('/order.html')


##@app.route('/shop/<int:id>', methods=['PUT'])
##def update(id):
     ##mycursor, connection = ProductDAO.get_cursor()
     
##@app.errorhandler(404)

##def not_found(error):
    ##return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)