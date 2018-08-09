from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash

#database connection
import os
import sqlite3
from passlib.hash import pbkdf2_sha256 #hash
path_db = os.getcwd() + '/db/flask_db.db'
DATABASE = path_db
SECRET_KEY = 'development key' #secure sessions of client-side

class Bill:
	def dis_bill(self):
		conn = sqlite3.connect(DATABASE)
		cli_id = session['id']
		cursor1 = conn.execute('select NUMBER from NUMBERS where ID_CLIENT=?',[cli_id])
		cursor2 = conn.execute('select PROG_NAME from IDP where ID_CLIENT=?',[cli_id])
		cursor3 = conn.execute('select CHARGE from BILLS where ID_CLIENT=?',[cli_id])
		number = [dict(number=row[0]) for row in cursor1.fetchall()]
		prog_name = [dict(prog_name=row[0]) for row in cursor2.fetchall()]
		charge = [dict(charge=row[0]) for row in cursor3.fetchall()]
		conn.close()
		welc_user = session['username']
		return render_template('clientpl.html',number=number,prog_name=prog_name,charge=charge,welc=welc_user)
		
