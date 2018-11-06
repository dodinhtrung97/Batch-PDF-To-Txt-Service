from Constants import DOWNLOAD_DIR, UPLOAD_DIR
import Object
import os
import tarfile
import Request as req

def extract_tgz(host, bucket_name, object_name):
    archive_name = object_name + ".tgz"
    archive_path = f"./{DOWNLOAD_DIR}/{archive_name}"
    archive_extract_path = f'./{UPLOAD_DIR}'

    Object.download(host, bucket_name, archive_name)
    with tarfile.open(archive_path, 'r:gz') as archive:
        archive.extractall(archive_extract_path, members=[file for file in archive.getmembers() if file.name.endswith(".pdf")])

    # Upload then clean-up
    for pdf_name in os.listdir(archive_extract_path):
        Object.upload(host, bucket_name, pdf_name)
        os.remove(f"{archive_extract_path}/{pdf_name}")
    os.remove(archive_path)

    req.extraction_status_update(bucket_name, object_name)

    return "Success"