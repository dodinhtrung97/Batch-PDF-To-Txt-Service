from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import Task
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

@app.route("/<bucketName>/<objectName>", methods=['POST'])
def handle_tgz_upload_request(bucketName, objectName):
	"""
	File upload route for frontend
	Because browser doesn't allow to set Content-Length header
	"""
	if not request.json:
		return Response("{'message': 'Blank body'}", status=400, mimetype='application/json')

	req_data = request.json
	file_md5 = req_data['fileMd5']
	print(file_md5)
	file_size = req_data['fileSize']
	file_data = req_data['data']


	result = Task.handle_file_upload(bucketName, objectName, file_data, file_md5, file_size)
	# send upload success message through socket
	with app.app_context():
		socketio.emit('status_update', '1')

	return result

@socketio.on('connect')
def socket_connect():
	print(f"Socket {request.sid}: connected")
	time.sleep(1)
	emit('test', "A test message")

@socketio.on('disconnect')
def socket_disconnect():
	print(f"Socket {request.sid}: disconnected")

@socketio.on_error_default
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=7075)