import sqlite3
import Admin
import Users
import Seller
import Client
import Bill
import os

from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash

	

#initializes the database for me to the application....
from contextlib import closing


#configuration for db
path_db = os.getcwd() + '/db/flask_db.db'
DATABASE = path_db
DEBUG=True

SECRET_KEY = 'development key' #secure sessions of client-side

#create our app :)
app = Flask(__name__)
app.config.from_object(__name__)

#database

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])#name of our db

		
#sec layer of 3-tier....
@app.route('/')
def index():
	#return redirect(url_for('bill'))
	return render_template('index.html')


@app.route('/user_login',methods=['POST','GET'])
def user_login():
	
	user = Users.Users()
	#if not session.get('logged_in'):
	return user.login()
	#else:
	#	return redirect(url_for('admin_control'))
	

@app.route('/user_logout')
def user_logout():
	session.pop('logged_in',None)
	#flash('You were logged out')
	#return redirect(url_for('index'))
	return render_template('index.html')


@app.route('/otp_control', methods=['POST','GET'])
def otp_control():
	if request.form['ot-pass'] == session['otp']:
		session['logged_in'] = True#true 
		if session['xar'] == 'admin':
			return redirect(url_for('admin_control'))
		elif session['xar'] == 'seller':
			return redirect(url_for('seller_control'))
		elif session['xar'] == 'client':
			return redirect(url_for('client_control'))
	else:
		error = 'Wrong one-time password'
		return render_template('index.html',error=error)

#admin
#from login the first time
@app.route('/admin_control', methods=['GET','POST'])
def admin_control():
	if not session.get('logged_in'):
		#abort(401)
		return redirect(url_for('user_login'))
	welcome_user = session['username']
	return render_template('admin.html',welc=welcome_user)

@app.route('/admin_add_programms', methods=['GET','POST'])
def admin_add_programms():
	if not session.get('logged_in'):
		#abort(401)
		return redirect(url_for('user_login'))
	welc = session['username']
	return render_template('adminap.html',welc=welc)

@app.route('/admin_see_programms', methods=['GET','POST'])
def admin_see_programms():
	if not session.get('logged_in'):
		#abort(401)
		return redirect(url_for('user_login'))
	conn = connect_db()
	cursor = conn.execute('select * from PROGRAMS')
	programs = [dict(name_prog=row[1], minute=row[2], sms=row[3], mb=row[4], euro=row[5]) for row in cursor.fetchall()]
	conn.close()
	welc = session['username']
	return render_template('adminsp.html',programs=programs,welc=welc)

	
@app.route('/admin_add_users', methods=['GET','POST'])
def admin_add_users():
	if not session.get('logged_in'):
		#abort(401)
		return redirect(url_for('user_login'))
	welc = session['username']
	return render_template('katclient.html',welc=welc)
	
@app.route('/admin_action',methods=['GET','POST'])
def admin_action():
	#return "OK"
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	if request.form['action'] == 'see':
		conn = connect_db()
		cursor = conn.execute('select * from PROGRAMS')
		programs = [dict(name_prog=row[1], minute=row[2], sms=row[3], mb=row[4], euro=row[5]) for row in cursor.fetchall()]
		conn.close()
		welc = session['username']
		return render_template('adminsp.html',programs=programs,welc=welc)
	elif request.form['action'] == 'add':
		admin = Admin.Admin()
		return admin.add_program()
	elif request.form['action']== 'add_user':
		admin = Admin.Admin()
		return admin.add_user()
	#never used!
	elif request.form['action'] == 'add_cli':
		admin = Admin.Admin()
		return admin.add_cli()
	elif request.form['action'] == 'back':
		return redirect(url_for('admin_control'))
	else: return "ok"


#client
@app.route('/client_control')
def client_control():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	welcome_user = session['username']
	return render_template('client.html',welc=welcome_user)
	

@app.route('/client_profile',methods=['GET','POST'])
def client_profile():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	client = Client.Client()
	return client.show_bill()
		
@app.route('/client_history',methods=['GET','POST'])
def client_history():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	client = Client.Client()
	return client.show_history()

@app.route('/client_action',methods=['GET','POST'])
def client_action():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	if request.form['action'] == 'see_bill':
		#return session['username']
		#return ID
		client = Client.Client()
		return client.show_bill()
	elif request.form['action'] == 'history':
		client = Client.Client()
		return client.show_history()
	elif request.form['action'] == 'pay':
		welcome_user = session['username']
		client = Client.Client()
		return client.pay_bill()
		
#seller	

	
@app.route('/seller_control')
def seller_control():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	welcome_user = session['username']
	return render_template('seller.html',welc=welcome_user)

@app.route('/seller_add_cli', methods=['GET','POST'])
def seller_add_cli():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	welc = session['username']
	return render_template('katclient_seller.html',welc=welc)
	
@app.route('/seller_change_prog', methods=['GET','POST'])
def seller_change_prog():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	welc = session['username']
	return render_template('sellercp.html',welc=welc)
	
@app.route('/seller_account_client', methods=['GET','POST'])
def seller_account_client():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	seller = Seller.Seller()
	return seller.version_account()
	
@app.route('/seller_action',methods=['GET','POST'])
def seller_action():
	if not session.get('logged_in'):
		return redirect(url_for('user_login'))
	if request.form['action'] == 'add_cli':
		#return "MPLAMPLA"
		seller = Seller.Seller()
		return seller.add_client()
	elif request.form['action'] == 'ac_cli':
		seller = Seller.Seller()
		return seller.version_account()
	elif request.form['action'] == 'change_prog':
		seller = Seller.Seller()
		return seller.change_program()
	elif request.form['action'] == 'back':
		return redirect(url_for('seller_control'))



if __name__ == '__main__':   
	app.run('127.0.0.1', debug=True, port=5000, ssl_context=('server.crt', 'file.key'))
	#app.run(debug=True,threaded=True)


	
