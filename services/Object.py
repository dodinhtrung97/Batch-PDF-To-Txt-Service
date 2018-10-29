import requests
import os
import time
import Request
from Constants import DOWNLOAD_DIR, UPLOAD_DIR

def download(host, bucket_name, object_name):
    url = f'http://{host}/{bucket_name}/{object_name}'
    for n in range(3):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                if not os.path.exists(DOWNLOAD_DIR):
                    os.makedirs(DOWNLOAD_DIR)
                with open(f"./{DOWNLOAD_DIR}/{object_name}", 'wb') as f:
                    f.write(r.content)
            # Invalid bucket/object name, let the error propagate
            break
        except:
            if n == 2: raise
            time.sleep(10)
    return f"./{DOWNLOAD_DIR}/{object_name}"

def upload(host, bucket_name, txt_name):
    Request.url = f"http://{host}/"
    for n in range(3):
        try:
            # Just try to upload and ignore errors
            Request.createUploadTicket(bucket_name, txt_name)
            Request.uploadFile(bucket_name, txt_name, 1, f"./{UPLOAD_DIR}")
            Request.completeUploadTicket(bucket_name, txt_name)
            break
        except:
            if n == 2: raise
            time.sleep(10)
