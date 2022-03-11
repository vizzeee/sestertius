import yaml
import json

def loader(method):
	def wrapper(*args, **kwargs):
		print(f'[Sestertius] {method.__name__}', end="... ", flush=True)
		operation_success = method(*args, **kwargs)
		msg = 'ok' if operation_success else 'error'
		print(msg)
	return wrapper

class Config:
	def load_yml(filename):
		with open(f'{filename}.yml', 'r') as file:
			cfg = yaml.safe_load(file)
		return cfg

class Save:
	def as_json(file, data):
		with open(file, 'w', encoding='utf-8') as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
			