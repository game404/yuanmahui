import redis


def test_get_set():
	r = redis.Redis(host='localhost', port=6379, db=0)
	print(r.set('foo', 'bar'))  # True
	print(r.get('foo')) # b'bar'


def test_pipline():
	r = redis.Redis(host='localhost', port=6379, db=0)
	pipe = r.pipeline()
	result =pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute()
	print(result)  # [True, True, 6]


def test_lua_script():
	r = redis.Redis(host='localhost', port=6379, db=0)
	lua = """
local value = redis.call('GET', KEYS[1])
value = tonumber(value)
return value * ARGV[1]
"""
	multiply = r.register_script(lua)
	r.set('foo', 2)
	result = multiply(keys=['foo'], args=[5]) 
	print(result) # 10



if __name__ == '__main__':
	test_lua_script()