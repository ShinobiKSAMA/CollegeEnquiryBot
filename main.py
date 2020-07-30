from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import aiml
import modules.backend as b
import modules.auth as auth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'EnqChatBot'

mysql = MySQL(app)
botName = "Enquiry Chat-Bot"

@app.route('/', methods=['GET', 'POST'])
def home():
	if 'user' in session:
		return redirect(url_for('bot'))
	if 'admin' in session:
		return redirect(url_for('dashboard'))
	return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
	try:
		if request.method == 'POST':
			email = request.form['email']
			psw = request.form['pass']
			
			res = auth.login(email, psw, mysql)
			if res is not None:
				session['user'] = res[0]
				return redirect(url_for('bot'))
			else:
				msg = "Wrong Credentials"
				return render_template("login.html", msg=msg)
	except Exception as e:
		return redirect(url_for('home'))
	return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
	try:
		if request.method == 'POST':
			usr = request.form['fname']
			email = request.form['email']
			psw = request.form['pass1']
			cpsw = request.form['pass2']
			
			if psw == cpsw:
				res = auth.register(usr, email, psw, mysql)
				print(res)
				return render_template("login.html", suc_msg=res)
			else:
				msg = "Password Does Not Match"
				return render_template("login.html", msg=msg)
	except Exception as e:
		print(e)
		return render_template("login.html")
	return render_template("login.html")

@app.route('/adm_Login', methods=['GET', 'POST'])
def login_adm():
	if 'admin' in session:
		return redirect(url_for('dashboard'))
	try:
		if request.method == 'POST':
			adm = request.form['adm']
			psw = request.form['pass']
				
			res = auth.login_adm(adm, psw, mysql)
			if res is not None:
				session['admin'] = 'admin'
				return redirect(url_for('dashboard'))
			else:
				msg = "Wrong Credentials"
				return render_template("adm_Login.html", msg=msg)
	except Exception as e:
		return redirect(url_for('login_adm'))
	return render_template("adm_Login.html")

@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user', None)
		return redirect(url_for('home'))
	elif 'admin' in session:
		session.pop('admin', None)
		return redirect(url_for('login_adm'))
	else:
		return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
	if 'admin' in session:
		db = auth.getUsers(mysql)
		return render_template("dashboard.html", db=db)
	return redirect(url_for('home'))

@app.route('/bot')
def bot():
	if 'user' in session:
		global botName
		k.learn("std-startup.xml")
		k.respond("load aiml b")

		chat = auth.getChat(session['user'], mysql)
		return render_template("botScreen.html", chat=chat)	
	return redirect(url_for('home'))

@app.route("/get")
def get_bot_response():
	userText = request.args.get('msg')
	print(userText)
	auth.add_msg(userText, session['user'], 0, mysql)
	botText = str(b.start(userText, k))
	auth.add_msg(botText, session['user'], 1, mysql)
	
	return botText

@app.route("/delUsr", methods=['POST'])
def delUsr():
	if request.method=='POST':
		usr = request.form['usr']
		res = auth.delUser(usr, mysql)
		if res[0] == 1:
			return jsonify(success=True)
		else:
			return jsonify(success=False)

k = aiml.Kernel()

if __name__ == '__main__':
    app.debug = True
    app.run()