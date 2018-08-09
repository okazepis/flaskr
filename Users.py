from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash

#database connection
import os
import sqlite3
from passlib.hash import pbkdf2_sha256 #hash
import OTP

path_db = os.getcwd() + '/db/flask_db.db'
DATABASE = path_db
SECRET_KEY = 'development key' #secure sessions of client-side


class Users:
	usersCounter = 0
	def __init__(self):
		#print "Constructor for Users!"
		Users.usersCounter += 1

	def setName(self, new_name):#an den valeis to self sou girnaei error
		self.name = new_name
	def getName(self):
		return self.name
		
		
	def setUsername(self,new_username):
		self.username = new_username
	def getUsername(self):
		return self.username
		
		
	def setSurname(self, new_surname):
		self.surname = new_surname
	def getSurname(self):
		return self.surname
		
		
	def setAttr(self, new_attr):
		self.attr = new_attr
	def getAttr(self):
		return self.attr

	def login(self):	
		error = None#watch this....
		
		if request.method == 'POST':
			conn = sqlite3.connect(DATABASE)
			in_loop = False
			try_name = request.form['username']
			try_pass = request.form['password']
			try_attr = request.form['attr']
			if not try_name or not try_pass:
				error = "You need to fill all the fields!"
				return render_template('index.html',error=error)
			if try_attr == "admin":
				cursor = conn.execute('select * from ADMINS where USERNAME=?',[try_name])
			elif try_attr == "seller":
				cursor = conn.execute('select * from SELLERS where USERNAME=?',[try_name])
			elif try_attr == "client":
				cursor = conn.execute('select * from CLIENTS where USERNAME=?',[try_name])
			
			for row in cursor:
				in_loop = True
				what_about_pass = pbkdf2_sha256.verify(try_pass,row[2])
				
				if what_about_pass == False:
					error = "Invalid password"
					return render_template('index.html',error=error)
				#if request.form['attr'] == row[3] and what_about_pass == True:#einai autos pou leei...
				#what are u ??
				if request.form['attr'] == "admin" and what_about_pass:
					#session['logged_in'] = True#pige sto flaskr/otp_control
					session['username'] = row[1]
					session['id'] = row[0]

					session['email'] = row[5]
					session['xar'] = 'admin'#to xaraktiristiko tou
					conn.close()#den theloume tin sindesi allo...
					session['otp'] = OTP.function_otp(session['email'])#steile email enan random 5psifio
					
					return render_template('otp.html')
				elif request.form['attr'] == "seller" and what_about_pass:
					#session['logged_in'] = True#pige sto flaskr/otp_control
					session['username'] = row[1]
					session['id'] = row[0]
					session['email'] = row[5]
					session['xar'] = 'seller'#to xaraktiristiko tou
					conn.close()#den theloume tin sindesi allo...
					session['otp'] = OTP.function_otp(session['email'])#steile email enan random 5psifio
					
					return render_template('otp.html')
				elif request.form['attr'] == "client" and what_about_pass:
					#session['logged_in'] = True#pige sto flaskr/otp_control
					session['username'] = row[1]
					session['id'] = row[0]
					session['email'] = row[5]
					session['xar'] = 'client'#to xaraktiristiko tou
					conn.close()#den theloume tin sindesi allo...
					session['otp'] = OTP.function_otp(session['email'])#steile email enan random 5psifio
					
					return render_template('otp.html')
			
			if in_loop == False:
				error = "Invalid username or attritube!"#not in loop
				return render_template('index.html',error=error)
			else:#useless else
				error = None
				return render_template('index.html',error=error)
			
			#return render_template('login.html',error=error)
		return render_template('index.html',error=error)
			
		
