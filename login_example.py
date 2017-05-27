#--* coding: utf-8 *--#
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'dblogin' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dblogin'

mongo = PyMongo(app)

@app.route('/')
def index():
	if 'username' in session:
		return 'You are logged as ' + session['username']

	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		# Set os objetos da colletion users do mongodb
		users = mongo.db.users
		# Busca dos dados do username informado
		login_user = users.find_one({'username' : request.form['username']})

		if login_user:
			# Verifica as senhas criptografadas
			if  sha256_crypt.verify(str(request.form['password']),login_user['password']):
				session['username'] = request.form['username']
				return redirect(url_for('index'))

		return 'Invalid username/password combination!!!'

	return render_template('login.html')

		
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=30)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
	# Recebe todos os objetos do formulario
	form = RegisterForm(request.form)
	# Verifica o metodo e valida os campo do formulario
	if request.method == 'POST' and form.validate():
		# Atribuicao de valores nas variaveis
		name = form.name.data 
		username = form.username.data
		passhash = sha256_crypt.encrypt(str(form.password.data))
		# Set os objetos da colletion users do mongodb
		users = mongo.db.users
		# Busca username ja cadastrado
		user_find = users.find_one({'username' : username})

		# Não havendo username cadastra, realiza o cadastro e abre uma session
		if user_find is None:
			users.insert({'name' : name, 'username' : username, 'password' : passhash })
			session['username'] = form.username.data
			return redirect(url_for('index'))

		return 'That username already exists!!!'

	return render_template('register.html', form=form)


if __name__ == '__main__':
	app.secret_key = 'loginsecret'
	app.run(debug=True)