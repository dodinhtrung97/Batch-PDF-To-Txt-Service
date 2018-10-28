import moviepy.editor as mp
import requests
import os
import time
import Request
from constant import Constants

def download(host, bucket_name, object_name):
    url = f'http://{host}/{bucket_name}/{object_name}'
    for n in range(3):
        try:
            r = requests.get(url)
            if not os.path.exists(Constants.DOWNLOAD_DIR):
                os.makedirs(Constants.DOWNLOAD_DIR)
            with open(f"./{Constants.DOWNLOAD_DIR}/{object_name}", 'wb') as f:
                f.write(r.content)
            break
        except:
            if n == 2: raise
            time.sleep(10)
    return f"./{Constants.DOWNLOAD_DIR}/{object_name}"

def upload(host, bucket_name, txt_name):
    Request.url = f"http://{host}/"
    for n in range(3):
        try:
            Request.createUploadTicket(bucket_name, txt_name)
            Request.uploadFile(bucket_name, txt_name, 1, r"./" + Constants.UPLOAD_DIR)
            Request.completeUploadTicket(bucket_name, txt_name)
            break
        except:
            if n == 2: raise
            time.sleep(10)
