from constant.Constants import DOWNLOAD_DIR, UPLOAD_DIR
import Object
import ast
import Request
import tarfile
import os

def get_txt_names(host, bucket_name):
    Request.url = f"http://{host}/"
    bucket_info = Request.listBucket(bucket_name)
    objects = ast.literal_eval(bucket_info.content.decode("utf-8"))["objects"]
    txt_names = [object["name"] for object in objects if object["name"].endswith(".txt")]
    return txt_names

def pack_txt_in_bucket(host, bucket_name, archive_name):
    txt_names = get_txt_names(host, bucket_name)
    archive_converted_name = archive_name + "_converted" + ".tgz"
    archive_converted_path = f"{UPLOAD_DIR}/{archive_converted_name}"
    # Download and pack the archive
    with tarfile.open(archive_converted_path, "w") as archive_converted:
        for txt_name in txt_names:
            Object.download(host, bucket_name, txt_name)
            txt_path = f"{DOWNLOAD_DIR}/{txt_name}"
            archive_converted.add(txt_path, arcname=f"{txt_name}")
            os.remove(txt_path)
    Object.upload(host, bucket_name, archive_converted_name)
    os.remove(archive_converted_path)

    return "Success"