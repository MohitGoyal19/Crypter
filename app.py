from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import jwt
import math
import os
import pymongo
from string import ascii_letters, digits
import time
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename


mongo = pymongo.MongoClient('localhost', 27017)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.secret_key = 'secret_key'

if not 'fernet.key' in os.listdir(os.getcwd()):
	fernet_key = Fernet.generate_key()

	with open('fernet.key', 'wb') as mykey:
		mykey.write(fernet_key)

else:
	with open('fernet.key', 'rb') as mykey:
	    fernet_key = mykey.read()

fernet = Fernet(fernet_key)

ascii_table_string = list(ascii_letters + digits + ':$!')
ascii_table_file = list(ascii_letters + digits)


def login_user(user):
	return jwt.encode({**user, 'expiration': time.time()+86400}, app.secret_key, algorithm='HS256')


def verify_login(request):
	if len(request.cookies) > 0:
		token = list(request.cookies.keys())[0]

		if token:
			details = jwt.decode(token.split(':', 1)[-1], app.secret_key, algorithms=['HS256'])
			
			if 'username' in details and mongo['local']['user'].find({'username': details['username']}) and details['expiration'] > time.time():
				return True

	return False


def get_user(request):
	return jwt.decode(list(request.cookies.keys())[0].split(':', 1)[-1], app.secret_key, algorithms=['HS256'])['username']


def get_hash(request):
	return jwt.decode(list(request.cookies.keys())[0].split(':', 1)[-1], app.secret_key, algorithms=['HS256'])['password']


def matrixize(data, matrix=[]):
	if len(data) < 1:
		return matrix
	
	if len(data) == 1:
		matrix.append([data])
		
		return matrix 
	
	size = int(math.sqrt(len(data)))
	matrix.append(list(data[:size**2]))

	return matrixize(data[size**2:], matrix)


def obfuscate_string(data):
	obfuscated_string = ''

	counter = 0
	while data and len(data) >= counter:
		if len(data[counter]) > 0:
			obfuscated_string = obfuscated_string + data[counter].pop(0)
		
		if len(data[counter]) == 0:
			data.pop(counter)

		else:
			counter += 1

		if counter == len(data):
			counter = 0

	return obfuscated_string


def matrix_to_list(matrices):
	return [elem for matrix in matrices for elem in matrix ]


def matrix_to_string(matrices):
	return ''.join([elem for matrix in matrices for elem in matrix ])


def encrypt(source, token, key, source_type='text'):
	data = source

	if isinstance(data, str) and source_type == 'text':
		data = matrixize(key+data, [])
		data = obfuscate_string(data)
		data = matrixize(data, [])
		data = matrix_to_list(data)

		for x in range(0, len(data)):
			data[x] = ascii_table_string[(ascii_table_string.index(data[x]) + ascii_table_string.index(token[x%len(token)])) % len(ascii_table_string)]

		return matrix_to_string(data)
	
	elif source_type == 'file':
		with open(source, 'rb') as f:
			data = f.read()

		data = fernet.encrypt(data)

		source_dir, file_name = os.path.split(source)

		file_name = list(file_name)
		for x in range(0, len(file_name)):
			if file_name[x] in ascii_table_file and token[x%len(token)] in ascii_table_file:
				file_name[x] = ascii_table_file[(ascii_table_file.index(file_name[x]) + ascii_table_file.index(token[x%len(token)])) % len(ascii_table_file)]

		file_name = ''.join(file_name)

		file_path = os.path.join(source_dir, file_name)
		with open(file_path, 'wb') as f:
			f.write(data)

		return file_path


def decrypt(source, token, key, source_type='text'):
	data = source
	length = len(data)
	arr = []
	while math.sqrt(length) > 0:
		arr.append(int(math.sqrt(length))**2)
		length -= (int(math.sqrt(length))**2)

	if isinstance(data, str) and source_type == 'text':
		data = list(data)
		
		for x in range(0, len(data)):
			if ascii_table_string.index(token[x%len(token)]) - ascii_table_string.index(data[x]) > 0:
				data[x] = ascii_table_string[len(ascii_table_string) - ascii_table_string.index(token[x%len(token)]) + ascii_table_string.index(data[x])]  
			
			else: 
				data[x] = ascii_table_string[ascii_table_string.index(data[x]) - ascii_table_string.index(token[x%len(token)])]

		matrix = []
		
		while sum(arr) > 0:
			for x in range(len(arr)):
				if len(matrix) <= x:
					matrix.append([])
				
				if arr[x] > 0:
					matrix[x].append(data.pop(0))
					arr[x] -= 1

		data = matrix_to_list(matrix)
		
		return ''.join(data)[len(key):]
	
	elif source_type == 'file':
		with open(source, 'rb') as f:
			data = f.read()

		data = fernet.decrypt(data)

		source_dir, file_name = os.path.split(source)

		file_name = list(file_name)
		for x in range(0, len(file_name)):
			if file_name[x] in ascii_table_file and token[x%len(token)] in ascii_table_file:		
				if ascii_table_file.index(token[x%len(token)]) - ascii_table_file.index(file_name[x]) > 0:
					file_name[x] = ascii_table_file[len(ascii_table_file) - ascii_table_file.index(token[x%len(token)]) + ascii_table_file.index(file_name[x])]  
				
				else: 
					file_name[x] = ascii_table_file[ascii_table_file.index(file_name[x]) - ascii_table_file.index(token[x%len(token)])]
				
		file_name = ''.join(file_name)

		file_path = os.path.join(source_dir, file_name)
		with open(file_path, 'wb') as f:
			f.write(data)

		return file_path


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	# logout_user()
	return redirect(url_for('/'))


@app.route('/', methods=['GET'])
def index():
	if verify_login(request):
		return redirect(url_for('crypter'))
	
	return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		payload = request.form

		if 'username' in payload and 'password' in payload:
			if mongo['local']['user'].find_one({'username': payload['username']}):
				response = jsonify({
					'status': 200,
					'message': 'User logged in successfully',
					'token': login_user({'username': payload['username'], 'password': generate_password_hash(payload['password'])})
				})

				response.status_code = 200

				return response
			
	response = jsonify({
		'status': 406,
		'message': 'A user with this username/e-mail already exists, please login'
	})

	response.status_code = 406

	return response


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

			response = jsonify({
				'status': 200,
				'message': 'User created successfully',
				'token': login_user({'username': payload['username'], 'password': generate_password_hash(payload['password'])})
			})
			# response = make_response(render_template('crypter.html'))
			
			return response
		
		else:
			response = jsonify('Invalid details for user registation, please try again')
			response.status_code = 403

			return response


@app.route('/crypter', methods=['GET'])
def crypter():
	if verify_login(request):
		return render_template('crypter.html')
	
	return redirect(url_for('/'))


@app.route('/crypt/text', methods=['POST'])
def crypt_text():
	if verify_login(request):
		if request.form['crypt_type'] == 'encrypt':
			response = jsonify({
				'status': 200,
				'message': f"String encrypted successfully, encrypted string is: '{encrypt(request.form['text'], get_hash(request), request.form['key'])}'",
			})
			response.status_code = 200

		elif request.form['crypt_type'] == 'decrypt':
			response = jsonify({
				'status': 200,
				'message': f"String decrypted successfully, decrypted string is: '{decrypt(request.form['text'], get_hash(request), request.form['key'])}'",
			})

			response.status_code = 200

		else:
			response = jsonify({
				'status': 401,
				'message': f"Invalid option",
			})

			response.status_code = 401

		return response	
	
	return redirect(url_for('/'))


@app.route('/crypt/file', methods=['POST'])
def crypt_file():
	if verify_login(request):
		mongo['local']['files'].insert_one({'user': get_user(request), 'filename': request.files['file'].filename, 'timestamp': time.time()})

		f = request.files['file']
		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)

		file_path = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
		f.save(file_path)

		if request.form['crypt_type'] == 'encrypt':
			return send_file(encrypt(file_path, get_hash(request), '', 'file'), as_attachment=True)
		
		elif request.form['crypt_type'] == 'decrypt':
			return send_file(decrypt(file_path, get_hash(request), '', 'file'), as_attachment=True)

		else:
			response = jsonify({
				'status': 401,
				'message': f"Invalid option",
			})

			response.status_code = 401

			return response
		
	return redirect(url_for('/'))
	

@app.errorhandler(404)
def not_found(error=None):
	message = jsonify({
		'status': 404,
		'message': request.url + ' Not Found'
	})

	message.status_code = 404

	return message


app.run(debug=True)