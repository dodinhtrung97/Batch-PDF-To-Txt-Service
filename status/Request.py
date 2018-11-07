import requests
from Config import OBJECT_HOST, OBJECT_PORT, SERVER_HOST, SERVER_PORT

OBJECT_URL = f'http://{OBJECT_HOST}:{OBJECT_PORT}'
SERVER_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

def handle_file_extract(bucket_name, object_name):
	object_name_no_ext = object_name.rsplit('.', 1)[0]
	requestUrl = f'{SERVER_URL}/extract?bucket_name={bucket_name}&object_name={object_name_no_ext}'
	requests.post(requestUrl)

def handle_file_convert(bucket_name):
	bucket_content = []

	r = requests.get(f'{OBJECT_URL}/{bucket_name}?list')
	response_json = r.json()
	object_list = response_json['objects']

	for object in object_list:
		file_extension = object['name'].rsplit('.', 1)[1]
		# Only convert pdfs
		if file_extension == 'pdf':
			bucket_content.append(object['name'])

	for object_name in bucket_content:
		object_name_no_ext = object_name.rsplit('.', 1)[0]
		requestUrl = f'{SERVER_URL}/convert?bucket_name={bucket_name}&object_name={object_name_no_ext}'
		requests.post(requestUrl)

	return bucket_content

def handle_file_pack(bucket_name):
	# object_name = bucket_name
	# So that resulting tgz will have bucket_name as prefix
	requestUrl = f'{SERVER_URL}/pack?bucket_name={bucket_name}&object_name={bucket_name}'
	requests.post(requestUrl)

	return bucket_name