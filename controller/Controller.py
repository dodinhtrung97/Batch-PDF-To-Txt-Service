from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import Task
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

"""Extract '{object_name}.tgz' found in {bucket_name} and upload all pdfs in the archive to that bucket"""
@app.route("/extract", methods=['POST'])
def handle_extraction_request():
	### OBJECT NAME WITHOUT FILE EXTENSION ###
	result = Task.enqueue_job("extract", [request.args.get("bucket_name"), request.args.get("object_name")])
	return result

"""Convert the '{object_name}.pdf' found in {bucket_name} and upload it to that bucket as '{object_name}.txt' """
@app.route("/convert", methods=['POST'])
def handle_conversion_request():
	### OBJECT NAME WITHOUT FILE EXTENSION ###
	result = Task.enqueue_job("convert", [request.args.get("bucket_name"), request.args.get("object_name")])
	return result

"""Pack all text files in {bucket_name} and upload to that bucket as '{object_name}_converted.tgz' """
@app.route("/pack", methods=['POST'])
def handle_packing_request():
	### OBJECT NAME WITHOUT FILE EXTENSION ###
	result = Task.enqueue_job("pack", [request.args.get("bucket_name"), request.args.get("object_name")])
	return result

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
	file_size = req_data['fileSize']
	file_data = req_data['data']

	result = Task.handle_file_upload(bucketName, objectName, file_data, file_md5, file_size)
	# send upload success message through socket
	message = {'status':'1'}
	message_json = json.dumps(message)
	with app.app_context():
		socketio.emit('status_update', message_json)

	return result

@socketio.on('connect')
def socket_connect():
	print("Client connected")

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=7072, threaded=True)