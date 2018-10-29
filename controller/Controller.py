from flask import Flask, request
from services import ConverterService
from services import Object
from constant.Constants import REDIS_HOST, REDIS_PORT, OBJECT_HOST
from flask_cors import CORS
from rq import Queue
from redis import Redis
import time

app = Flask(__name__)
CORS(app)
conn = Redis(REDIS_HOST, REDIS_PORT)
q = Queue('conversion', connection=conn)

@app.route("/convert/<bucket_name>/<pdf_name>/<txt_name>", methods=['POST'])
def convert_pdf_to_txt(bucket_name, pdf_name, txt_name):
	pdf_file_path = Object.download(OBJECT_HOST, bucket_name, pdf_name)
	# enqueue job
	job = q.enqueue_call(func=ConverterService.pdf_to_text, args=(pdf_name, txt_name,))
	# poll until job is done
	while job.result is None:
		time.sleep(0.1)

	Object.upload(OBJECT_HOST, bucket_name, txt_name)
	# Send post request to main server here