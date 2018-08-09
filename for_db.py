import sqlite3
from passlib.hash import pbkdf2_sha256
import os

#kwdikoi gia users
code1 = pbkdf2_sha256.encrypt("admin",rounds=20000,salt_size=16)
code2 = pbkdf2_sha256.encrypt("admin",rounds=20000,salt_size=16)
code3 = pbkdf2_sha256.encrypt("admin",rounds=20000,salt_size=16)

path = os.getcwd() + '/db/flask_db.db'


conn = sqlite3.connect(path)
#dimiourgia users
conn.execute('insert into ADMINS(ID,USERNAME,PASSWORD,LAST_NAME,FIRST_NAME,EMAIL) \
				VALUES(?,?,?,?,?,?)',[1,'ADMIN',code1,'kazepis','orfeas','fakeeee@gmaill.com'])
conn.execute('insert into SELLERS(ID,USERNAME,PASSWORD,LAST_NAME,FIRST_NAME,EMAIL) \
			VALUES(?,?,?,?,?,?)',[1,'SELLER',code2,'SURNAME','FIRSTNAME','fakeeee2@gmaill.com'])
conn.execute('insert into CLIENTS(ID,USERNAME,PASSWORD,LAST_NAME,FIRST_NAME,EMAIL,ADDRESS,CITY,POSTCODE,AFM)\
			 VALUES(?,?,?,?,?,?,?,?,?,?)',[1,'Butcher',code3,'BEEF','FEED','fakeeee2@gmaill.com','Random Street','Random City',12345,123456789])


#3 programs
conn.execute('insert into PROGRAMS(PROG_NAME,MINUTES,SMS,MB,EURO) VALUES(?,?,?,?,?)',["ALL_600",600,600,600,8])
conn.execute('insert into PROGRAMS(PROG_NAME,MINUTES,SMS,MB,EURO) VALUES(?,?,?,?,?)',["ALL_200",200,200,200,3])
conn.execute('insert into PROGRAMS(PROG_NAME,MINUTES,SMS,MB,EURO) VALUES(?,?,?,?,?)',["1000MIN+200SMS",1000,200,0,4])

#gia ton client
conn.execute('insert into NUMBERS(ID_CLIENT,NUMBER) VALUES(?,?)',[1,6999999999])
conn.execute('insert into NUMBERS(ID_CLIENT,NUMBER) VALUES(?,?)',[2,6900000000])
conn.execute('insert into CALLS(ID_CLIENT,MIN,SMS,MB) values(?,?,?,?)',[1,403,54,2004])
conn.execute('insert into CALLS(ID_CLIENT,MIN,SMS,MB) values(?,?,?,?)',[2,40,5,200])
conn.execute('insert into IDP(ID_CLIENT,PROG_NAME) values(?,?)',[1,"ALL_600"])
conn.execute('insert into IDP(ID_CLIENT,PROG_NAME) values(?,?)',[2,"1000MIN+200SMS"])
conn.execute('insert into BILLS(ID_CLIENT,CHARGE) values(?,?)',[1,14])
conn.execute('insert into BILLS(ID_CLIENT,CHARGE) values(?,?)',[2,6])
conn.commit()
conn.close()
