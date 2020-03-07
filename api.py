from flask import Flask,render_template,request,redirect,url_for,session
from models.model import user_exists,save_user,product_exists,add_product,products_list,remove_from_db,add_to_cart,cart_info,remove_from_cart
app=Flask(__name__)
app.secret_key='hello'

@app.route('/')
def home():

	return render_template('home.html')

@app.route('/about')

def about():

	return  render_template('about.html',title='hii')


@app.route('/contact')

def contact():

	return  render_template('contact.html',title='about :3')

@app.route("/login",methods=['GET','POST'])

def login():
	if request.method=='POST':
	 		
	 		username=request.form['username']
	 		password=request.form['password']

	 		result=user_exists(username)
	 		if result:
	 			if result['password']!=password:
	 				return "password doesnot match .Go back and enter a new password"
	 			session['username']=username
	 			session['c_type']=result['c_type']
	 			return(redirect(url_for('home')))
	 		return "user name doesnot exists"
	return redirect(url_for('home'))
@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=='POST':


		user_info={}
		#import pdb;pdb.set_trace()
		user_info['username']=request.form['username']
		user_info['password']=request.form['password1']
		password2=request.form['password2']
		user_info['c_type']=request.form['type']
		if user_info['c_type']=='buyer':
			user_info['cart']=[]	
		if user_exists(user_info['username']):
			return "user already exists"
		if user_info['password']!=password2:
			return "passwords dont match"
		save_user(user_info)
		return redirect(url_for('home'))
	return redirect(url_for('home'))

@app.route('/products',methods=['GET','POST'])
def products():
	if request.method=='POST':
		product_info={}
		product_info['name']=request.form['name']
		product_info['price']=int(request.form['price'])
		product_info['description']=request.form['description']
		product_info['seller']=session['username']

		if product_exists(product_info['name']):
			return "products exists"
		add_product(product_info)
		return redirect(url_for("products"))
	return render_template('products.html',products=products_list())
@app.route('/remove_products',methods=['GET','POST'])
def remove_products():
	if request.method=='POST':
		name=request.form['name']
		remove_from_db(name)
		return redirect(url_for('products'))
	return redirect(url_for('products'))	
@app.route('/cart',methods=['GET','POST'])
def cart():
	if request.method=='POST':
		name=request.form['name']
		add_to_cart(name)
		return redirect(url_for('cart'))
	products=cart_info()
	return render_template('cart.html',products=products)
@app.route('/remove_cart',methods=['GET','POST'])
def remove_cart():
	if request.method=='POST':
		name=request.form['name']
		remove_from_cart(name)
		return redirect(url_for('cart'))
	return redirect(url_for('products'))	

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))
	


app.run(debug=True)	
