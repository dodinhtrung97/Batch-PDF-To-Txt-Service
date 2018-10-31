from redis import Redis
from rq import Queue
from Config import OBJECT_HOST, OBJECT_PORT, REDIS_HOST, REDIS_PORT
import Response as res
import requests

conn = Redis(REDIS_HOST, REDIS_PORT)
q = Queue("pdf", connection=conn)
q_failed = Queue("failed", connection=conn)
q_failed.empty() # Clear the failed queue everytime server is restarted

host = f"{OBJECT_HOST}:{OBJECT_PORT}"
bucket_host = "http://webapp:5000/"
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

def createBucket(bucketName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'create': ''}
    r = requests.post(bucket_host + bucketName, params=params)
    return r

def createUploadTicket(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'create': ''}
    requestUrl = bucket_host + "{}/{}".format(bucketName, objectName)
    r = requests.post(requestUrl, params=params)
    return r

def completeUploadTicket(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'complete': ''}
    requestUrl = bucket_host + "{}/{}".format(bucketName, objectName)
    r = requests.post(requestUrl, params=params)
    return r

def uploadFile(bucketName, objectName, part, data, md5File, fileSize, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'partNumber': part}
    requestUrl = bucket_host + "{}/{}".format(bucketName, objectName)
    headers = {'Content-Length': str(fileSize), 'Content-MD5': md5File}
    r = requests.put(requestUrl, data=data, headers=headers, params=params)
    return r, md5File, fileSize

def handle_file_upload(bucket_name, object_name, data, md5, size):
    createBucket(bucket_name)
    createUploadTicket(bucket_name, object_name)
    uploadFile(bucket_name, object_name, 1, data, md5, size)
    completeUploadTicket(bucket_name, object_name)

    return 'Upload Success'