import is_afm

from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash

#database connection
import os
import sqlite3
from passlib.hash import pbkdf2_sha256 #hash
path_db = os.getcwd() + '/db/flask_db.db'
DATABASE = path_db
SECRET_KEY = 'development key' #secure sessions of client-side

import Users
class Seller(Users.Users):
	def add_client(self):
		if request.method == 'POST':
			welcome_user = session['username']
			error_for_add_user = None
			flag_add = False
			conn = sqlite3.connect(DATABASE)
			
			username = request.form['username']	
			password = request.form['password']
			con_pass = request.form['con_password']
			lname = request.form['lname']
			fname = request.form['fname']	
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
				return render_template('katclient_seller.html',error_for_add_user=error_for_add_user,welc=welcome_user)
			if password != con_pass:
				error_for_add_user = "Passwords not match!"
				return render_template('katclient_seller.html',error_for_add_user=error_for_add_user,welc=welcome_user)
			
			for_afm = is_afm.is_afm()
			error_for_add_user, flag_afm = for_afm.is_afm(str(afm))#for error=None || 9 digit, flag=True||False
			if flag_afm == False:
				return render_template('katclient_seller.html',error_for_add_user=error_for_add_user,welc=welcome_user)
				
			#lets insert a new client!
			password = pbkdf2_sha256.encrypt(password,rounds=20000,salt_size=16)
			conn.execute('insert or ignore into CLIENTS\
					(USERNAME,PASSWORD,LAST_NAME,FIRST_NAME,EMAIL,ADDRESS,CITY,POSTCODE,AFM)\
					 VALUES(?,?,?,?,?,?,?,?,?)',[username,password,lname,fname,email,address,city,postcode,afm])
			conn.commit()
			#other tables for clients!!
			cursor = conn.execute('select ID FROM CLIENTS WHERE USERNAME=? and last_name=? \
								and first_name=? and email=?',[username,lname,fname,email])#for id
			id_temp = None
			for row in cursor:
				id_temp = row[0]
				break
			if id_temp is not None:
				#id_temp = int(id_temp)
				conn.execute("insert into NUMBERS(ID_CLIENT,NUMBER) values(?,?)",[id_temp,number])
				#conn.execute('insert into BILLS(ID_CLIENT,CHARGE) VALUES(?,?)',[id_temp,0])#avoid error payment!!!
				#id -> autoincrement giauto leipei to id apo to insert query...	
				#return str(id_temp)
				error_for_add_user = "A new client added!"
				conn.commit()

			#check if insert is done!!!
			cur = conn.execute('select * from clients where username=? and last_name=? \
										and first_name=? and email=?',[username,lname,fname,email])
			for r in cur:
				flag_add = True
				error_for_add_user="A new client added!"
				break
				
			if flag_add == False:
				error_for_add_user = "Username exists!"
			
			conn.close()
			return render_template('katclient_seller.html',error_for_add_user=error_for_add_user,\
													welc=welcome_user)
			
	def version_account(self):
		welcome_user = session['username']
		msg = None
		client_found = False#flag for client
		conn = sqlite3.connect(DATABASE)
		username = request.form['username']
		if not username:
			msg = 'You need fill all the fields!'
			return render_template('sellercp.html',msg=msg,welc=welcome_user)
		username = str(username)
		#find the client!
		cur = conn.execute('select ID FROM CLIENTS WHERE USERNAME=?',[username])
		for row in cur:
			client_found = True
			cli_id = row[0]
		if client_found == False:
			msg = 'This client does\'n existis'
			return render_template('sellercp.html',msg=msg,welc=welcome_user)
			
		#lets take element!
		cursor0 = conn.execute('select * from CLIENTS where ID=?',[cli_id])
		cursor1 = conn.execute('select NUMBER from NUMBERS where ID_CLIENT=?',[cli_id])
		cursor2 = conn.execute('select PROG_NAME from IDP where ID_CLIENT=?',[cli_id])
		cursor3 = conn.execute('select CHARGE from BILLS where ID_CLIENT=?',[cli_id])
		cursor4 = conn.execute('select * from CALLS where ID_CLIENT=?',[cli_id])
		info = [dict(lname=row[3],fname=row[4],email=row[5],\
						addr=row[6],city=row[7],post=row[8],afm=row[9]) for row in cursor0.fetchall()]
		number = [dict(number=row[0]) for row in cursor1.fetchall()]
		prog_name = [dict(prog_name=row[0]) for row in cursor2.fetchall()]
		charge = [dict(charge=row[0]) for row in cursor3.fetchall()]
		history = [dict(minute=row[1],sms=row[2],mb=row[3]) for row in cursor4.fetchall()]
		conn.close()
		return render_template('sellercp.html',info=info,
		number=number,prog_name=prog_name,charge=charge,\
									history=history,welc=welcome_user)
		
		
	def change_program(self):
		welcome_user = session['username']
		MSG = None
		client_found = False
		program_found = False
		username = request.form['username']
		
		new_prog = request.form['new_prog']
		if not username or not new_prog:
			MSG = "You need to fill all the fields!"
			return render_template('sellercp.html',MSG=MSG,welc=welcome_user)
		username = str(username)
		new_prog = str(new_prog)
		conn = sqlite3.connect(DATABASE)
		#find client
		cur = conn.execute('select ID from CLIENTS where USERNAME=?',[username])
		for row in cur:
			cli_id = row[0]
			client_found = True#true only if we'll go to loop
		
		if client_found == False:
			MSG = "Client not found!"
			return render_template('sellercp.html',MSG=MSG,welc=welcome_user)
		#find program
		euro_for_new_program = 0#charge for the new program
		cur = conn.execute('select PROG_NAME,EURO from PROGRAMS where PROG_NAME=?',[new_prog])
		new_prog_update = ""
		for row2 in cur:
			new_prog_update = row2[0] #program's name
			program_found = True#true only....
			euro_for_new_program = row2[1]#for update. Add the previous charge with the next!
			
		if program_found == False:
			MSG = "This program doesn't exists!"
			return render_template('sellercp.html',MSG=MSG,welc=welcome_user)
		
		
		#new client or not.....?
		client_reg = str(request.form['reg'])
		if client_reg == 'old':
			#update for client which already have program!
			#CHARGE MUST ADDED WITH THE NEXT
			previous_charge = 0 #charge for previous program
			cur = conn.execute('select CHARGE from BILLS where ID_CLIENT=?',[cli_id])
			for row3 in cur:
				previous_charge = row3[0]#charge
			
			charge = previous_charge + euro_for_new_program
		
			conn.execute('update IDP set PROG_NAME=? where ID_CLIENT=?',[new_prog_update,cli_id])
			conn.execute('update BILLS set CHARGE=? where ID_CLIENT=?',[charge,cli_id])
			conn.commit()
			conn.close()
		elif client_reg == 'new':
			conn.execute('INSERT INTO IDP(ID_CLIENT,PROG_NAME) VALUES(?,?)',[cli_id,new_prog_update])
			conn.execute('insert into BILLS(ID_CLIENT,CHARGE) VALUES(?,?)',[cli_id,euro_for_new_program])
			conn.commit()
			conn.close()
		#add really change for mistake!!!
		return render_template('sellercp.html',MSG="The update is done!",welc=welcome_user)
