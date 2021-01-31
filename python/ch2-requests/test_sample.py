import requests
import json

def test_requests_get():
	r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
	print(r.status_code) # 200
	print(r.headers['content-type']) # 'application/json; charset=utf8'
	print(r.encoding) # 'utf-8'
	print(r.text) # '{"type":"User"...'
	print(r.json()) # {'private_gists': 419, 'total_private_repos': 77, ...}

def test_json_pretty_print():
	a = {
        "name": "game404",
        "age": 2
    }
	print(json.dumps(a)) # {"name": "game404", "age": 2}
	print(json.dumps(a, sort_keys=True, indent=2))  # 定义indent参数
	"""
	{
	  "age": 2,
	  "name": "game404"
	}
	"""

def test_structures():
	a = {
    	"name":"game404"
	}
	# print(a.name)  # AttributeError
	print(a["name"])