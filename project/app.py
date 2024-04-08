
from flask import Flask, url_for, request, redirect, abort, session, render_template, jsonify
from markupsafe import escape


app = Flask(__name__, static_url_path='', static_folder='static')
import stripe 
from DataDAO import DataDAO
from ProductDAO import ProductDAO



    
@app.route('/')
def index():
    ##if 'username' in session:
        ##return 'Logged in as %s' % escape(session['username']) +\
        ##'<br><a href="'+'/home.html'+'">home</a>' +\
        ##'<br><a href="'+url_for('admin')+'">Admin</a>'
        ##return '<br><a href="'+'/home.html'+'">home</a>' 
          return app.send_static_file('home.html')
      


    
@app.route('/admin',methods=['GET'])
def adminOnly():
    if 'username' in session:
        return render_template("/admin.html")
    elif not 'username' in session:
        return redirect(url_for('login'))
    
@app.route('/shop', methods =['GET'])
def product_list():
    products = get_products()
    return render_template('shop.html', products=products)


    
@app.route('/products', methods = ['GET'])
def get_all():
    try:
        results = ProductDAO.getAll()
        return jsonify(results)
    except Exception as e:
        print(f"Error getting products: {e}")
        abort(500)
        
@app.route('/product/<int:id>', methods=['GET'])
def findById(id):
    try:
        foundProduct = ProductDAO.findByID(id)
        if foundProduct:
            return jsonify(foundProduct)
        else:
            abort(404)
    except Exception as e:
        print(f"Error finding Product with id {id}: {e}")
        abort(500)
        

    

@app.route('/order', methods = ["GET"])
def get_order():
    if 'username' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'username' in session:
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

@app.route('/order/<int:id>', methods=['DELETE'])
def deleteorder(id):
    try:
        OrderDAO.delete(id)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting order with id {id}: {e}")
        abort(500)
    
    
    
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

        if username in users and users[username][1] == password:
            session['username'] = username
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
      



@app.route('/failure')
def failure():
    return "the payment failed please try again and make payment"
    return redirect('/order.html')


@app.route('/shop/<int:id>', methods=['PUT'])
def update(id):
     mycursor, connection = ProductDAO.get_cursor()
     
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)