from redis import Redis
from rq import Queue
from Config import OBJECT_HOST, OBJECT_PORT, REDIS_HOST, REDIS_PORT
import Response as res

conn = Redis(REDIS_HOST, REDIS_PORT)
q = Queue("pdf", connection=conn)
q_failed = Queue("failed", connection=conn)
q_failed.empty() # Clear the failed queue everytime server is restarted

host = f"{OBJECT_HOST}:{OBJECT_PORT}"
jobs = {"extract": "ExtractorService.extract_tgz",
        "convert" : "ConverterService.pdf_to_text",
        "pack": "PackerService.pack_txt_in_bucket"}

def enqueue_job(job_name, args):
    bucket_name, object_name = args
    try:
        job_id = f"{job_name}/{bucket_name}/{object_name}"
        if job_id not in q.job_ids:
            q_failed.remove(job_id) # If we enqueue a job that failed, that means we are retrying and have therefore handle the error
            q.enqueue_call(func=jobs[job_name], args=[host] + args, result_ttl=30, timeout="1h", job_id=job_id)
        # If it fail (e.g. exception raise, the job will automatically be put in the failed queue
        return res.success
    except Exception as e:
        return res.makeErrorResponse(400, "Error", str(e))