#--* coding: utf-8 *--#
from flask import Flask 
#from flask.ext.pymongo import PyMongo 
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'dbfabiomac'
#app.config['MONGO_URI'] = 'mongodb://fabiomac:mrcx741a@ds029436.mlab.com:29436/dbfabiomac'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dbfabiomac'


mongo = PyMongo(app)


@app.route('/')
def index():
	return 'Hello Flask!'

@app.route('/add')
def add():
	users = mongo.db.users
	users.insert({'name' : 'Fabio', 'language' : 'Python' })
	users.insert({'name' : 'Maria Eduarda', 'language' : 'C' })
	users.insert({'name' : 'Spock', 'language' : 'Ruby' })
	users.insert({'name' : 'Antony', 'language' : 'C++' })
	return 'Added User!!!'

@app.route('/find')
def find():
	users = mongo.db.users
	spock = users.find_one({'name' : 'Spock'})
	return 'You found ' + spock['name'] + '. His favorite language is ' + spock['language']


@app.route('/update')
def update():
	users = mongo.db.users
	spock = users.find_one({'name' : 'Spock'})
	spock['language'] = 'JavaScript'
	users.save(spock)
	return 'Update Spock!!!'

@app.route('/delete')
def delete():
	users = mongo.db.users
	fabio = users.find_one({'name' : 'Fabio'})
	users.remove(fabio)
	return 'Removed Spock!!!'

if __name__ == '__main__':
	app.secret_key = 'mrcx741a'
	app.run(debug=True)