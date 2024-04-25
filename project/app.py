import os
from flask import Flask, url_for, request, redirect, abort, session, render_template, jsonify
from markupsafe import escape
import stripe 
from DataDAO import DataDAO
from ProductDAO import ProductDAO
from OrderDao import OrderDao
from AdminDao import AdminDao

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LbowdF35qyiz7dHw0XaoOZmq8UHUmdBRYN1BGuQjSwfvoXH42Lx2Vm6c7x28VHik0Kd8KzAdmnBXbzwsEDTCsq500PRbcO9QB'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LbowdF35qyiz7dHoPZ46KJW0xEwnmWR7oBwSZQ3sTe8xHx69ane3dG1FwrFLbyATOwtJRLtXisC6RwwDm0v19QD00ZgY8zh0u'
stripe.api_key = 'sk_test_51LbowdF35qyiz7dHoPZ46KJW0xEwnmWR7oBwSZQ3sTe8xHx69ane3dG1FwrFLbyATOwtJRLtXisC6RwwDm0v19QD00ZgY8zh0u'


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
        
@app.route('/admin',methods=['GET'])
def adminOnly():
    if 'email' in session:
        return render_template("/admin.html")
    elif not 'email' in session:
        return redirect(url_for('login'))
    
@app.route('/admin/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        # Call the delete method from the productDAO to delete the product
        AdminDao.delete(id)
        return jsonify({"message": f"Admin with ID {id} deleted successfully"})
    except Exception as e:
        # Handle any exceptions that may occur during deletion
        return jsonify({"error": f"Error deleting admin with ID {id}: {str(e)}"}), 500

        
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
def delete_order(id):
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
        OrderDao.update((update_order['email'], update_order['amount'], update_order['eircode'], id))
        
        return jsonify({"message": f"Product with ID {id} updated successfully"})
    except Exception as e:
        # Handle any exceptions that may occur during the update
        return jsonify({"error": f"Error updating product with ID {id}: {str(e)}"}), 500
    
    
    
@app.route('/contact')
def contact():
     return app.send_static_file('contact.html')

 
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
   

@app.route('/buy')
def buy():
    '''
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1GtKWtIdX0gthvYPm4fJgrOr',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    '''
    return render_template(
        'index.html', 
        #checkout_session_id=session['id'], 
        #checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'YOUR_PRODUCT_PRICE_ID',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}
if __name__ == '__main__':
    app.run(debug=True)