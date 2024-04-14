
from flask import Flask, url_for, request, redirect, abort, session, render_template, jsonify
from markupsafe import escape


app = Flask(__name__, static_url_path='', static_folder='static')
import stripe 
from DataDAO import DataDAO
from ProductDAO import ProductDAO
from BandDAO import BandDAO



    
@app.route('/')
def index():
    ##if 'username' in session:
        ##return 'Logged in as %s' % escape(session['username']) +\
        ##'<br><a href="'+'/home.html'+'">home</a>' +\
        ##'<br><a href="'+url_for('admin')+'">Admin</a>'
        ##return '<br><a href="'+'/home.html'+'">home</a>' 
          return app.send_static_file('home.html')
      


    
@app.route('/admin', methods=['GET'])
def adminOnly():
    if 'username' in session:
        return render_template("/admin.html")
    elif not 'username' in session:
        return redirect(url_for('login'))
    
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
        
    
    
    
@app.route('/shop', methods =['GET'])
def product_list():
    products = get_product()
    return render_template('shop.html', products=products)


    
@app.route('/product', methods=['GET'])
def get_product():
    try:
        results = ProductDAO.getAll()
        return jsonify(results)
    except Exception as e:
        print(f"Error getting products: {e}")
        abort(500)
        
@app.route('/product/<int:pid>', methods=['PUT'])
def update(pid):
    foundProduct = ProductDAO.findByID(pid)
    if not foundProduct:
        abort(404)

    if not request.json:
        abort(400, 'Missing JSON in request')

    try:
        ProductDAO.update(pid, request.json)
        return jsonify(request.json)
    except Exception as e:
        print(f"Error updating Product with id {pid}: {e}")
        abort(500)
        
@app.route('/product/<int:pid>', methods=['GET'])
def findById(pid):
   try:
        foundProduct = ProductDAO.findByID(pid)
        if foundProduct:
            return jsonify(foundProduct)
        else:
            abort(404)
   except Exception as e:
       print(f"Error finding Product with id {pid}: {e}")
       abort(500)
        
@app.route('/product/<int:pid>', methods=['DELETE'])
def delete(pid):
    try:
        ProductDAO.delete(pid)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting product with the id {pid}: {e}")
        abort(500)
        
@app.route('/band', methods =['GET'])
def all_bands():
    products = get_all_bands()
    return render_template('shop.html')

        
@app.route('/band/', methods=['GET'])
def get_all_bands():
    try:
        results = BandDAO.getAll()
        return jsonify(results)
    except Exception as e:
        print(f"Error getting bands: {e}")
        abort(500)
        
@app.route('/band/<int:pid>', methods=['PUT'])
def update(pid):
    foundProduct = BandDAO.findByID(id)
    if not foundProduct:
        abort(404)

    if not request.json:
        abort(400, 'Missing JSON in request')

    try:
        BandDAO.update(id, request.json)
        return jsonify(request.json)
    except Exception as e:
        print(f"Error updating Product with id {id}: {e}")
        abort(500)
        
@app.route('/band/<int:id>', methods=['GET'])
def findById(id):
   try:
        foundProduct = BandDAO.findByID(id)
        if foundProduct:
            return jsonify(foundProduct)
        else:
            abort(404)
   except Exception as e:
       print(f"Error finding Product with id {id}: {e}")
       abort(500)
        
@app.route('/band/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        BandDAO.delete(id)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting product with the id {id}: {e}")
        abort(500)


@app.route('/order', methods = ["GET"])
def get_order():
    if 'name' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'name' in session:
        return redirect(url_for('login'))
    ##try:
        ##results = OrderDAO.getAll()
        ##return jsonify(results)
    ##except Exception as e:
        print(f"Error getting your orders: {e}")
        abort(500)
        
##@app.route('/order/<int:id>', methods=['GET'])
##def findById(id):
    ##try:
        ##foundOrder = OrderDAO.findByID(id)
        ##if foundOrder:
            ##return jsonify(foundOrder)
        ##else:
            ##abort(404)
    ##except Exception as e:
        print(f"Error finding Product with id {id}: {e}")
        abort(500)

##@app.route('/order/<int:id>', methods=['DELETE'])
##def deleteorder(id):
    ##try:
        ##OrderDAO.delete(id)
        ##return jsonify({"done": True})
    ##except Exception as e:
        ##print(f"Error deleting order with id {id}: {e}")
        ##abort(500)
    
    
    
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
        username = request.form.get("name")
        password = request.form.get("password")

        if name in customer and customers[username][1] == password:
            session['name'] = name
            return redirect(url_for('admin'))
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