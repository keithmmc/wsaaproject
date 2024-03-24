
from flask import Flask, url_for, request, redirect, abort, session, render_template
from markupsafe import escape

app = Flask(__name__, static_url_path='', static_folder='static')
import stripe 

    
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

    
@app.route('/products', methods =['GET'])
def products():
    return 'products'

@app.route('/shop', methods =['GET'])
def product_list():
    products = get_products()
    return render_template('shop.html', products=products)
    

        

@app.route('/order')
def order():
    if 'username' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'username' in session:
        return redirect(url_for('login'))
    
@app.route('/contact')
def contact():
    return render_template(contact.html)

    
@app.route('/history')
def history():
    if 'username' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    else:
        return redirect(url_for('login'))
    
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




if __name__ == '__main__':
    app.run(debug=True)