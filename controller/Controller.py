from flask import Flask, request
from ..converter import ConverterService
from ..services import Request
from ..services import WorkerService
from ..constant import Comstants
from flask_cors import CORS
from rq import Queue
from rq.job import Job
from ..worker.Worker import conn
import time

app = Flask(__name__)
CORS(app)
q = Queue(connection=conn)

@app.route("/convert/<bucket_name>/<pdf_name>/<txt_name>", methods=['POST'])
def convert_pdf_to_txt(bucket_name, pdf_name, txt_name):
	pdf_file_path = WorkerService.download(Constants.HOST, bucket_name, pdf_name)
	# enqueue job
	job = q.enqueue_call(func=ConverterService.pdf_to_text, args=(pdf_name, txt_name,))
	# poll until job is done
	while job.result is None:
		time.sleep(0.1)

	WorkerService.upload(Constants.HOST, bucket_name, txt_name)
	# Send post request to main server here