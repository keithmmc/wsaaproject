
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
def shop():
    return 'shop'

        

@app.route('/order')
def order():
    if 'username' in session:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'username' in session:
        return redirect(url_for('login'))
    
@app.route('/history')
def history():
    if 'order' in order:
        return '<br><a href="'+'/order.html'+'">order</a>' 
    elif not 'order' in order:
        return redirect(url_for('order'))
    
   

@app.route('/process-payment', methods=['POST'])
def process_payment():
      payment_method_id = request.form.get('paymentMethodId')
      

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




@app.route('/failure')
def failure():
    return "the payment failed please try again and make payment"
    return redirect('/order.html')




if __name__ == '__main__':
    app.run(debug=True)