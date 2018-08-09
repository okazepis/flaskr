import Seller
import Client
import Users
import is_afm

#database connection
import os
import sqlite3
from passlib.hash import pbkdf2_sha256
path_db = os.getcwd() + '/db/flask_db.db'
DATABASE = path_db
SECRET_KEY = 'development key' #secure sessions of client-side

from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash


class Admin(Seller.Seller):
	Users.Users.usersCounter = Users.Users.usersCounter - 1#do not increase without real user!
		
	def add_user(self):
		if request.method == 'POST':
			flag_add = False
			welcome_user = session['username']
			error_for_add_user = None
			conn = sqlite3.connect(DATABASE)
			#sure data for all kind of users!!
			username = request.form['username']
			password = request.form['password']
			con_pass = request.form['con_password']
			lname = request.form['lname']
			fname = request.form['fname']
			attr = request.form['attr']
			if attr == "client":
				#only for clients!
				email = request.form['email']
				number =  request.form['number']
				afm = request.form['afm']
				address = request.form['address']
				postcode = request.form['postcode']
				city = request.form['city']
				if not username or not password or not con_pass or not lname or not fname or not email \
						or not number or not afm or not address or not city or not postcode:
					error_for_add_user = "You need fill all the fields!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				if password != con_pass:
					error_for_add_user = "Passwords not match!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				for_afm = is_afm.is_afm()
				error_for_add_user, flag_afm = for_afm.is_afm(str(afm))
				if flag_afm == False:
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				#lets insert a new client!
				password = pbkdf2_sha256.encrypt(password,rounds=20000,salt_size=16)
				conn.execute('insert or ignore into CLIENTS\
						(USERNAME,PASSWORD,LAST_NAME,FIRST_NAME,EMAIL,ADDRESS,CITY,POSTCODE,AFM)\
						 VALUES(?,?,?,?,?,?,?,?,?)',[username,password,lname,fname,email,address,city,postcode,afm])
				conn.commit()
				#other tables for clients!!
				cursor = conn.execute('select ID FROM CLIENTS WHERE USERNAME=?',[username])#for id
				id_temp = None
				for row in cursor:
					id_temp = row[0]
					break
				if id_temp is not None:#carefully
					id_temp = int(id_temp)
					conn.execute("insert into NUMBERS(ID_CLIENT,NUMBER) values(?,?)",[id_temp,number])
					conn.execute('insert into BILLS(ID_CLIENT,CHARGE) VALUES(?,?)',[id_temp,0])#avoid error payment!!!
			#id -> autoincrement -- that's why id missing from query ;)
				cur = conn.execute('select * from clients where username=? and last_name=? \
										and first_name=? and email=?',[username,lname,fname,email])
				for r in cur:
					flag_add = True
					error_for_add_user="A new client added!"
					break
			
			elif attr == "seller":
				if not username or not password or not con_pass or not lname or not fname:
					error_for_add_user = "You need fill all the fields!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				if password != con_pass:
					error_for_add_user = "Passwords not match!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				password = pbkdf2_sha256.encrypt(password,rounds=20000,salt_size=16)
				conn.execute("INSERT OR IGNORE INTO SELLERS(USERNAME,PASSWORD,LAST_NAME,FIRST_NAME)\
								VALUES(?,?,?,?)",[username,password,lname,fname])
								
				cur = conn.execute('select * from sellers where username=? and last_name=? \
										and first_name=?',[username,lname,fname])
				for r in cur:
					flag_add = True
					error_for_add_user="A new seller added!"
					break
			
			
			elif attr == "admin":
				if not username or not password or not con_pass or not lname or not fname:
					error_for_add_user = "You need fill all the fields!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				if password != con_pass:
					error_for_add_user = "Passwords not match!"
					return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
				password = pbkdf2_sha256.encrypt(password,rounds=20000,salt_size=16)
				conn.execute("INSERT OR IGNORE INTO ADMINS(USERNAME,PASSWORD,LAST_NAME,FIRST_NAME)\
								VALUES(?,?,?,?)",[username,password,lname,fname])
				
				cur = conn.execute('select * from admins where username=? and last_name=? \
										and first_name=?',[username,lname,fname])
				for r in cur:
					flag_add = True#just know if insert its done!
					error_for_add_user="A new admin added!"
					break
			
			if flag_add == False:
				error_for_add_user = "Username already exists!"
			conn.commit()
			conn.close()
			
			return render_template('katclient.html',error_for_add_user=error_for_add_user,welc=welcome_user)
		
	def add_cli(self):
		welcome_user = session['username']
		error_for_add_cli = None
		conn = sqlite3.connect(DATABASE)
		username = request.form['username']
		password = request.form['password']
		number = request.form['number']
		if not username or not password or not number:
			error_for_add_cli = "You need fill all the fields!"
			return render_template('for_admin.html',error_for_add_cli=error_for_add_cli,welc=welcome_user)
		username = str(username)
		password = str(password)
		number = int(number)							
		password = pbkdf2_sha256.encrypt(password,rounds=20000,salt_size=16)
		conn.execute("INSERT INTO CLIENTS(USERNAME,PASSWORD) VALUES(?,?)",[username,password])
		conn.commit()
		cursor = conn.execute('select ID FROM CLIENTS WHERE USERNAME=?',[username])
		for row in cursor:
			id_temp = row[0]
			break
		id_temp = int(id_temp)
		conn.execute("insert into NUMBERS(ID_CLIENT,NUMBER) values(?,?)",[id_temp,number])
		conn.execute('insert into BILLS(ID_CLIENT,CHARGE) VALUES(?,?)',[id_temp,0])#avoid error payment!!!
		conn.commit()
		conn.close()
		error_for_add_cli = "A new client added!"
		return render_template('for_admin.html',error_for_add_cli=error_for_add_cli,welc=welcome_user)
		
	def del_user(self):
		pass
		

		
	def add_program(self):
		if request.method == 'POST':
			welcome_user = session['username']
			error_for_add_prog = None
			#connect with the database
			conn = sqlite3.connect(DATABASE)
			name_prog = request.form['name_prog']
			
			#html5 type="number"
			#its integer!
			
			minute = request.form['minute']
			sms = request.form['sms']
			mb = request.form['mb']
			euro = request.form['euro']
			
			#avoid void
			if not name_prog or not minute or not sms or not mb or not mb or not euro:
				error_for_add_prog = "You need fill all the fields!"
				return render_template('adminap.html',error_for_add_prog=error_for_add_prog,welc=welcome_user)

			#goodbye sql injection :)
			conn.execute("INSERT OR IGNORE INTO PROGRAMS(PROG_NAME,MINUTES,SMS,MB,EURO) \
						VALUES (?,?,?,?,?)",[name_prog,minute,sms,mb,euro])
			conn.commit()#save the changes!
			conn.close()
			#return redirect(url_for('admin_control'))
			error_for_add_prog = "A new program added!"
			return render_template('adminap.html',error_for_add_prog=error_for_add_prog,\
								welc=welcome_user)
