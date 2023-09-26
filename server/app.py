from flask import Flask, request, jsonify
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = pymongo.MongoClient('localhost', 27017)

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/login', methods=['POST'])
def login():
	pass


@app.route('/register', methods=['POST'])
def register():
	payload = request.json

	if 'username' in payload and 'password' in payload:
		mongo['local']['user'].insert_one({'username': payload['username'], 'password': generate_password_hash(payload['password'])})

		response = jsonify('User register successfully')
		response.status_code = 201

		return response
	
	else:
		response = jsonify('Invalid details for user registation, please try again')
		response.status_code = 403

		return response


@app.errorhandler(404)
def not_found(error=None):
	message = jsonify({
		'status': 404,
		'message': request.url + ' Not Found'
	})

	message.status_code = 404

	return message


app.run(debug=True)