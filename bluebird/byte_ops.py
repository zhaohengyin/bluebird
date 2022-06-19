import json
import pickle
import base64
import ast


def serialize_object_to_string(obj):
	obj = pickle.dumps(obj)
	encoded = base64.b64encode(obj)
	encoded = encoded.decode('ascii')
	return encoded


def deserialize_string_to_object(string):
	decoded = base64.b64decode(string)
	return pickle.loads(decoded)


def encode_arg_dict(dict):
	result = {}
	for key, value in dict.items():
		result[key] = serialize_object_to_string(value)
	return json.dumps(result)


def decode_arg_dict(json_dict):
	dict = ast.literal_eval(json_dict)
	result = {}
	for key, value in dict.items():
		result[key] = deserialize_string_to_object(value)
	return result

