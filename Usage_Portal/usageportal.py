from flask import Flask, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SubscribersForm, MonthlyForm
from flask_mysqldb import MySQL
from flask import request
import mysql.connector
from datetime import datetime

#import pymysql
#pymysql.install_as_MySQLdb()
#import MySqldb
#conn=pymysql.connect("localhost","root","","dispur_assam")
#cursor= conn.cursor
app = Flask(__name__)

app.config['SECRET_KEY']='d526216e2a8fa16111496ef7902c790b'

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/dispur_assam'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dispur_assam'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dispur_assam"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM subscribes")

myresult = mycursor.fetchall()

mysql = MySQL(app)
db=SQLAlchemy(app)



@app.route('/')
@app.route('/home')
def home():
	# Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		if request.method == 'POST':
			details = request.form
			username = details['username']
			email = details['email']
			contact_number='9872135674'
			password=details['password']
			confirm_password=details['confirm_password']
			role_id='CUST1'
			cur = mysql.connection.cursor()
			cur.execute("""INSERT INTO users (User_Name, Email_ID, 
        				Contact_Number, Usr_Pwd, Usr_ConfirmPwd,Role_id) 
        				VALUES (%s, %s, %s, %s, %s, %s)""", (username, email, contact_number, password,confirm_password,role_id))
			mysql.connection.commit()
			cur.close()
			flash(f'Account created for {form.username.data}!','success')
			return redirect(url_for('home'))
	return render_template('register.html',title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		mycursor.execute('SELECT * FROM users WHERE Email_ID = %s AND Usr_Pwd = %s AND isRegistered=1', (form.email.data, form.password.data))
		account = mycursor.fetchone()
		if account:
			flash('You have been logged in!','success')
			userid=(account[0])
			session['loggedin'] = True
			session['id'] = account[0]
			session['email'] = account[3]
			if account[9]=='CUST1':
				return redirect(url_for('user',id=userid))	
			else:
				return redirect(url_for('employee'))
			#print(str(account[0]))
		else:
			flash('Login Unsuccessful.Please check email or password.','danger')
	return render_template('login.html',title='Login',form=form)

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/employee')
def employee():
	if 'loggedin' in session:
		#all_data = subscribes.query.all()

		return render_template('emp_main.html' ,employees=myresult)
	return redirect(url_for('login'))
@app.route('/add_new')
def add_new():
	if 'loggedin' in session:
		return render_template('add_new.html')
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))	
@app.route('/subscribes',methods=['GET','POST'])
def subscribes():
	if 'loggedin' in session:
		form=SubscribersForm()
		if form.validate_on_submit():
			if request.method == 'POST':
				details = request.form
				user_id = int(details['user_id'])
				plan_id = int(details['plan_id'])
				amount_payable = int(details['amount_payable'])
				date_of_call=str(details['date_Of_call'])
				call_duration=int(details['call_duration'])
				cur = mysql.connection.cursor()
	#			sql="INSERT INTO subscribes (U_ID, Plan_ID, Amount_Payable, Date_Of_Call, Call_Duration) VALUES (%s, %s, %s, %s, %s)"
	#			val=tuple([user_id, plan_id, amount_payable, date_of_call,call_duration])
	#			cur.execute(sql,val)
				cur.execute("INSERT INTO subscribes (U_ID,Plan_ID,Amount_Payable,Date_Of_Call,Call_Duration) VALUES (%s,%s,%s,%s,%s)",[user_id, plan_id,amount_payable,date_of_call,call_duration])  
				mysql.connection.commit()
				cur.close()
				flash(f'Details Added Successfully','success')
				return redirect(url_for('employee'))
		return render_template('subscribes.html',title='Subscriber', form=form)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

@app.route('/monthly',methods=['GET','POST'])
def monthly():
	if 'loggedin' in session:
		form=MonthlyForm()
		if form.validate_on_submit():
			if request.method == 'POST':
				details = request.form
				user_id = int(details['user_id'])
				plan_id = int(details['plan_id'])
				monthly_bill = int(details['monthly_bill'])
				cur = mysql.connection.cursor()
				cur.execute("INSERT INTO monthly_usage (U_ID,Plan_ID,monthly_usage) VALUES (%s,%s,%s)",[user_id, plan_id,monthly_bill])  
				mysql.connection.commit()
				cur.close()
				flash(f'Bill Generated Successfully','success')
				return redirect(url_for('employee'))
		return render_template('monthly.html',title='Monthly Bill', form=form)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

#This route is for deleting Subscriber details
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
	if 'loggedin' in session:
		if request.method == 'GET':
			#arg1=int(request.args['id'])
			mycursor.execute("DELETE FROM subscribes where U_ID = %s;",[id])
			#mydb.session.delete(id)
			mydb.commit()
			flash("Subscriber Deleted Successfully")
			return redirect(url_for('employee'))
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

@app.route('/user/<id>/', methods= ['GET','POST'])
def user(id):
	if 'loggedin' in session:
		if request.method == 'GET':
			mycursor.execute("""SELECT User_Name,monthly_usage from users inner join 
				monthly_usage on users.U_ID = monthly_usage.U_ID where users.U_ID = %s""",[id])
			myresult = mycursor.fetchone()
			#print(myresult)
			mydb.commit()
			return render_template('usersearch.html', id=id, user=myresult)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

@app.route('/userplans/<id>', methods=['GET','POST'])
def userplans(id):
	if 'loggedin' in session:
		if request.method == 'GET':
			mycursor.execute("""SELECT users.U_ID, users.User_Name, subscribes.Date_Of_Call,
			 subscribes.Call_Duration, subscribes.Amount_Payable 
				from users inner join 
				subscribes on users.U_ID = subscribes.U_ID where users.U_ID = %s""",[id])
			myresult = mycursor.fetchall()
			print(myresult)
			mydb.commit()
			return render_template('userplans.html', id=id, title="User Plans", transactions=myresult)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
	if 'loggedin' in session:
		email=session['email']
		mycursor.execute('SELECT * FROM users WHERE Email_ID = %s',[email])
		account = mycursor.fetchone()
		userid=account[0]
		if account[9]=='CUST1':
			return redirect(url_for('user',id=userid))
		else:
			return redirect(url_for('employee'))
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)