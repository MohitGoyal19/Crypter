from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for
import jwt
import math
import pymongo
import time
from werkzeug.security import generate_password_hash, check_password_hash


# from utils import encrypt, decrypt, login_user, verify_login


mongo = pymongo.MongoClient('localhost', 27017)

app = Flask(__name__)
app.secret_key = 'secret_key'



def login_user(response, user):
	token = jwt.encode({**user, 'expiration': time.time()+86400}, app.secret_key, algorithm='HS256')

	response.headers.set('Authorization', f"Bearer {token}")

	return response


def verify_login(token):
	details = jwt.decode(token.lstrip('Bearer '), app.secret_key, algorithm='HS256')
	
	if 'username' in details and mongo['local']['user'].find({'username': details['username']}):
		return True

	return False


def get_hash(token):
	return jwt.decode(token.lstrip('Bearer '), app.secret_key, algorithm='HS256')['password']


def matrixize(data, matrix=[]):
	if len(data) == 1:
		return matrix.append([data])
	
	size = math.sqrt(len(data))

	return matrixize(data[size:], matrix.append(data[:size]))


def obfuscate(data):
	obfuscated_string = ''

	while data:
		for x in data:
			if len(data[x]) > 0:
				obfuscated_string = obfuscated_string + data[x].pop(0)

			data.pop(x)

	return obfuscated_string


def encrypt(data, token, key, source_type):
	if isinstance(data, str) and source_type == 'text':
		data = matrixize(data + get_hash(token))

	else:
		pass


def decrypt(data, token, key, source_type):
	if isinstance(data, str) and source_type == 'text':
		pass

	else:
		pass


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	# logout_user()
	return redirect(url_for('/'))


@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':
		return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		payload = request.form

		if 'username' in payload and 'password' in payload:
			if mongo['local']['user'].find_one({'username': payload['username']}):
				response = jsonify({
					'status': 406,
					'message': 'A user with this username/e-mail already exists, please login'
				})

				response.status_code = 406

				return response

			mongo['local']['user'].insert_one({'username': payload['username'], 'password': generate_password_hash(payload['password'])})

			response = make_response(render_template('crypter.html'))
			response = login_user(response, {'username': payload['username'], 'password': generate_password_hash(payload['password'])})
			

			print(response)
			
			return response
		
		else:
			response = jsonify('Invalid details for user registation, please try again')
			response.status_code = 403

			return response
		

@app.route('/encrypt/text', methods=['POST'])
def encrypt_text():
	response = jsonify({
		'status': 200
	})
	
	return response


@app.route('/encrypt/file', methods=['POST'])
def encrypt_file():
	return redirect(url_for('/crypter'))


@app.route('/decrypt/text', methods=['POST'])
def decrypt_text():
	return redirect(url_for('/crypter'))


@app.route('/decrypt/file', methods=['POST'])
def decrypt_file():
	return redirect(url_for('/crypter'))



@app.errorhandler(404)
def not_found(error=None):
	message = jsonify({
		'status': 404,
		'message': request.url + ' Not Found'
	})

	message.status_code = 404

	return message


app.run(debug=True)