def function_otp(email):	
	import smtplib
	import random
	from datetime import datetime
	from flask import Flask,request,session,g,redirect,url_for, \
	abort, render_template,flash

	TO = email

	SUBJECT = 'One-Time Password'

	random.seed(datetime.now())
	otp = random.randint(10000,99999)
	TEXT = str(otp)

	gmail_sender = 'orf_kaz_test@freemail.gr'
	gmail_passwd = ''#remember your password! It's a secret! armanis-7 by Antwnis

	server = smtplib.SMTP('smtp.freemail.gr',587)
	server.ehlo()
	server.starttls()
	server.ehlo
	server.login(gmail_sender,gmail_passwd)

	BODY = '\r\n'.join([
		'To: %s' % TO,
		'From: %s' % gmail_sender,
		'Subject: %s' % SUBJECT,
		'',
		TEXT
		])

	
	try:
		server.sendmail(gmail_sender, [TO], BODY)
		server.quit()
		return str(otp)
	except:
		error = 'Something wrong with email server. Please try later'
		return render_template('index.html',error=error)
