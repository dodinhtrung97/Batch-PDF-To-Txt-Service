from redis import Redis
from rq import Queue
from Config import OBJECT_HOST, OBJECT_PORT
import requests
import Response as res
import ast

bucket_host = f"http://{OBJECT_HOST}:{OBJECT_PORT}/"

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
    r = createBucket(bucket_name)
    response = ast.literal_eval(r.content.decode("utf-8"))
    if r.status_code == 400: return res.makeResponse(r.status_code, response)
    r = createUploadTicket(bucket_name, object_name)
    response = ast.literal_eval(r.content.decode("utf-8"))
    if r.status_code == 400: return res.makeResponse(r.status_code, response)
    r = uploadFile(bucket_name, object_name, 1, data, md5, size)[0]
    response = ast.literal_eval(r.content.decode("utf-8"))
    if r.status_code == 400: return res.makeResponse(r.status_code, response)
    r = completeUploadTicket(bucket_name, object_name)
    response = ast.literal_eval(r.content.decode("utf-8"))
    return res.makeResponse(r.status_code, response)