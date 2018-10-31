from flask import Flask, request
from flask_cors import CORS
import Task

app = Flask(__name__)
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
	if not request.json:
		return "Failure"

	req_data = request.json
	file_md5 = req_data['fileMd5']
	file_size = req_data['fileSize']
	file_data = req_data['data']

	result = Task.handle_file_upload(bucketName, objectName, file_data, file_md5, file_size)

	return result
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7072, threaded=True)