import requests
import os
import hashlib

url = ''

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def createBucket(bucketName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'create': ''}
    r = requests.post(url + bucketName, params=params)
    return r

def listBucket(bucketName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'list': ''}
    r = requests.get(url + bucketName, params=params)
    return r

def deleteBucket(bucketName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'delete': ''}
    r = requests.delete(url + bucketName, params=params)
    return r

def createUploadTicket(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'create': ''}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.post(requestUrl, params=params)
    return r

def completeUploadTicket(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'complete': ''}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.post(requestUrl, params=params)
    return r

def uploadFile(bucketName, objectName, part, uploadPath, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'partNumber': part}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    filePath = "{}/{}".format(uploadPath, objectName)
    fileSize = os.path.getsize(filePath)
    md5File = md5(filePath)
    headers = {'Content-Length': str(fileSize), 'Content-MD5': md5File}
    with open(filePath, 'rb') as f:
        r = requests.put(requestUrl, data=f, headers=headers, params=params)
    return r, md5File, fileSize

def deleteObjectPart(bucketName, objectName, part, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'partNumber': part}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.delete(requestUrl, params=params)
    return r

def deleteObject(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'delete': ''}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.delete(requestUrl, params=params)
    return r

def setObjectMeta(bucketName, objectName, key, value, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'metadata': '', 'key': key}
    data = {'value' : value}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.put(requestUrl, params=params, data=data)
    return r

def removeObjectMeta(bucketName, objectName, key, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'metadata': '', 'key': key}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.delete(requestUrl, params=params)
    return r

def getObjectMetaByKey(bucketName, objectName, key, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'metadata': '', 'key': key}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.get(requestUrl, params=params)
    return r

def getAllObjectMetas(bucketName, objectName, overrideParams=None):
    if overrideParams: params = overrideParams
    else: params = {'metadata': ''}
    requestUrl = url + "{}/{}".format(bucketName, objectName)
    r = requests.get(requestUrl, params=params)
    return r

def extraction_status_update(bucket_name, object_name):
    status = '2'
    requestUrl = f'http://status:7075/status/{bucket_name}/{object_name}/{status}'
    r = requests.post(requestUrl)
    return r