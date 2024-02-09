from flask import Flask,render_template,request,redirect, session
from flask_mail import Mail,Message
import mysql.connector
import os



app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="remotemysql.com", user="type your user_id", password="type your pwd", database="type your db_id")
cursor=conn.cursor()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='put your sender email_id'
app.config['MAIL_PASSWORD']='put your sender email_pwd'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)


@app.route('/')
def input():
	return render_template("login.html")
@app.route('/register')
def reg():
	return render_template("register.html")
@app.route('/home')
def home():
	if 'user_id' in session:
		return render_template("home.html")
	else:
		return redirect('/')
@app.route('/book')
def book():
	if 'user_id' in session:
		return render_template("book.html")
	else:
		return redirect('/')
@app.route('/cancel')
def cancel():
	if 'user_id' in session:
		return render_template("cancel.html")
	else:
		return redirect('/')
@app.route('/status')
def status():
	if 'user_id' in session:
		return render_template("status.html")
	else:
		return redirect('/')
@app.route('/message')
def message():
	if'user_id' in session:
		return render_template("message.html")
	else:
		return redirect('/')
@app.route('/userid')
def userid():
	if 'user_id' in session:
		return render_template('userid.html')
	else:
		return redirect('/')
@app.route('/login_validation', methods=['POST'])
def login_validation():
	email=request.form.get('email')
	password=request.form.get('password')
	cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
	users=cursor.fetchall()
	if len(users)>0:
		session['user_id']=users[0][0]
		return redirect('/home')
	else:
		return redirect('/')
@app.route('/add_user', methods=['POST'])
def add_user():
	name = request.form.get('uname')
	email = request.form.get('uemail')
	password = request.form.get('upassword')
	cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))
	conn.commit()
	return render_template("happy.html")
@app.route('/book_app',methods=['POST'])
def book_app():
	id=session['user_id']
	name=request.form.get('uname')
	status=request.form.get('ubook')
	if status=="uvalue":
		cursor.execute("""INSERT INTO `doctor1` (`booking_id`,`user_id`,`name`,`status`) VALUES (NULL,'{}','{}','{}')""".format(id,name,"Booked"))
		conn.commit()
		cursor.execute("""SELECT * FROM `doctor1` WHERE `name` LIKE '{}'""".format(name))
		books=cursor.fetchall()
		return "Booked Successfully and your booking id is {}".format(books[0][0])

@app.route('/book_app1',methods=['POST'])
def book_app1():
	id=session['user_id']
	name=request.form.get('uname1')
	status=request.form.get('ubook1')
	if status=="uvalue1":
		cursor.execute("""INSERT INTO `doctor2` (`booking_id`,`user_id`,`name`,`status`) VALUES (NULL,'{}','{}','{}')""".format(id,name,"Booked"))
		conn.commit()
		cursor.execute("""SELECT * FROM `doctor2` WHERE `name` LIKE '{}'""".format(name))
		books=cursor.fetchall()
		return "Booked Successfully and your booking id is {}".format(books[0][0])



@app.route('/cancel_app',methods=['POST'])
def cancel_app():
	id=request.form.get('bid')
	name=request.form.get('uname')
	status=request.form.get('ubook')
	cursor.execute("""SELECT * FROM `doctor1` WHERE `name` LIKE '{}' AND `booking_id` LIKE '{}'""".format(name,id))
	cancel1=cursor.fetchall()
	if status=="uvalue":
		if len(cancel1)==0:
			cursor.execute("""UPDATE `doctor2` SET `status`='{}' WHERE `name` LIKE '{}' AND `booking_id` LIKE '{}'""".format("Canceled",name,id))
			conn.commit()
			return render_template("sad.html")
		else:
			cursor.execute("""UPDATE `doctor1` SET `status`='{}' WHERE `name` LIKE '{}' AND `booking_id` LIKE '{}'""".format("Canceled",name,id))
			conn.commit()
			return render_template("sad.html")

@app.route('/status_app',methods=['POST'])

def status_app():
	name=request.form.get('uname')
	id=request.form.get('uid')
	cursor.execute("""SELECT * FROM `doctor1` WHERE `name` LIKE '{}' AND `booking_id` LIKE '{}'""".format(name,id))
	statuses=cursor.fetchall()
	if len(statuses)==0:
		cursor.execute("""SELECT * FROM `doctor2` WHERE `name` LIKE '{}' AND `booking_id` LIKE '{}'""".format(name, id))
		statuses1 = cursor.fetchall()
		return statuses1[0][3]
	else:
		return statuses[0][3]

@app.route('/datadis')
def datadis():
	cursor.execute("""SELECT * FROM `doctor1` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
	ids=cursor.fetchall()
	cursor.execute("""SELECT * FROM `doctor2` WHERE `user_id` LIKE '{}'""".format(session['user_id']))
	ids1 = cursor.fetchall()
	return "You have booked total {} bookings through our website".format(len(ids)+len(ids1))

@app.route('/send_message',methods=['GET','POST'])
def send_message():
	if request.method=="POST":
		subject = request.form['usubject']
		msg=request.form['message']
		message=Message(subject,sender="mukherjee.prithu@gmail.com",recipients=["srinjoymukherjeesphs@gmail.com"])
		message.body=msg
		mail.send(message)
		return "Message Sent"



@app.route('/logout')
def logout():
	session.pop('user_id')
	return redirect('/')




if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)