from flask import Flask, jsonify, Response

def makeResponse(statusCode, response):
    app = Flask(__name__)
    with app.app_context():
        json = jsonify(response)
        json.status_code = statusCode
        return json

def makeForbiddenNameResponse(key):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "{} name contains forbidden characters".format(key)})

def makeAlreadyExistResponse(key):
    return makeResponse(400,
                        {'status': "Error",
                         'message': '{} already exists'.format(key)})

def makeAlreadyDeletedResponse(key):
    return makeResponse(400,
                        {'status': "Error",
                         'message': '{} already deleted'.format(key)})

def makeDoesNotExistResponse(key):
    return makeResponse(400,
                        {'status': "Error",
                         'message': '{} does not exist'.format(key)})

def makeMissingRequiredResponse(key, value):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "Missing required {}: {}".format(key, value)})

def makeMissingPartsResponse(parts):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "Missing parts: {}".format(parts)})

def makeErrorResponse(statusCode, status, msg):
    return makeResponse(statusCode,
                        {'status': status,
                         'message': msg})

def makeMismatchedResponse(key):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "{} mismatched".format(key)})

def makePartsMD5MismatchedResponse(parts):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "Mismatched in md5 for following parts: {}".format(parts)})

def makeInvalidResponse(key, value):
    return makeResponse(400,
                        {'status': "Error",
                         'message': "Invalid value for {}: {}".format(key, value)})

success = makeResponse(200,
                       {'status': "Success"})
partNumberNotANumber = makeResponse(400,
                                    {'status': "Error",
                                     'message': "Part number is not a number"})
partNumberOutOfRange = makeResponse(400,
                                    {'status': "Error",
                                     'message': "Part number out of range"})
noFileSpecified = makeResponse(400,
                               {'status': "Error",
                                'message': "No file specified"})
noPartsUploaded = makeResponse(400,
                               {'status': "Error",
                                'message': "No parts uploaded"})
missingPartsMD5 = makeResponse(400,
                               {'status': "Error",
                                'message': "md5 of some parts are missing"})
uploadAlreadyDone = makeResponse(400,
                                 {'status': "Error",
                                  'message': "Upload is already done"})
uploadNotDone = makeResponse(400,
                             {'status': "Error",
                              'message': "Upload is not done"})