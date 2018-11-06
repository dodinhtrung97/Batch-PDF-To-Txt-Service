from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import Task
import time
import json
import Response as res

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

IP_TO_SIDS_DICT = {}
BUCKET_TO_IP_DICT = {}
STATUS_DICT = {}

@app.route("/<bucket_name>/<object_name>/<status>", methods=['POST'])
def handle_status_update(bucket_name, object_name, status):
	with app.app_context():
		# emit to all existing rooms
		socketio.emit('status_update', status)

	# Update status dict
	STATUS_DICT[request.remote_addr] = (bucket_name, status)

	return res.makeResponse(200, 
							{"status": "Success",
							 "bucketName": bucket_name, 
							 "objectName": object_name})

@app.route("/<bucketName>/<objectName>", methods=['POST'])
def handle_tgz_upload_request(bucketName, objectName):
	"""
	File upload route for frontend
	Because browser doesn't allow to set Content-Length header
	"""
	if not request.json:
		return Response("{'message': 'Blank body'}", status=400, mimetype='application/json')

	# Maps bucket_name to user's ip
	BUCKET_TO_IP_DICT[bucketName] = request.remote_addr
	# Initializes bucket status
	STATUS_DICT[request.remote_addr] = (bucketName, '0')

	req_data = request.json
	file_md5 = req_data['fileMd5']
	file_size = req_data['fileSize']
	file_data = req_data['data']

	result = Task.handle_file_upload(bucketName, objectName, file_data, file_md5, file_size)
	# send upload success message through socket
	with app.app_context():
		socketio.emit('status_update', '1')

	return result

@socketio.on('connect')
def socket_connect():
	"""
	Add request.sid to ip address's sid list
	"""
	print(f"Socket {request.sid}: connected")
	print(f"From IP: {request.remote_addr}")

	client_ip = request.remote_addr
	# Update key's value
	if client_ip in IP_TO_SIDS_DICT:
		sid_list = IP_TO_SIDS_DICT[client_ip]
		sid_list.append(request.sid)
		IP_TO_SIDS_DICT[client_ip] = sid_list
	else:
		IP_TO_SIDS_DICT[client_ip] = [request.sid]

	with app.app_context():
		socketio.emit('join', request.sid)

	time.sleep(1)

@socketio.on('room')
def on_join(room):
	"""
	Join private socketio room
	"""
	join_room(room)
	print(f"User {request.remote_addr} has joined room: {room}")

@socketio.on('disconnect')
def socket_disconnect():
	"""
	Remove request.sid from ip address
	"""
	client_ip = request.remote_addr
	sid_list = IP_TO_SIDS_DICT[client_ip]
	sid_list.remove(request.sid)
	IP_TO_SIDS_DICT[client_ip] = sid_list

	# Leave room
	leave_room(request.sid)

	print(f"Socket {request.sid}: disconnected")
	print(f"User {request.remote_addr} has left room: {request.sid}")

@socketio.on_error_default
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=7075)