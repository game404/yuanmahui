# yuanmahui

每周阅读一个项目源码。

* python
	1. redis
	2. requests
	3. bottle
	4. http-server
	5. wsgiref
* golang 


## 简单测试

```
cd python/ch1-redis
python test_sample.p
```

## 使用pytest

测试requests下所有用例:
```
cd python/ch2-requests
pytest -s
```
测试结果:
```
(.venv) ➜  ch2-requests git:(main) ✗ pytest -s
================================================= test session starts ==================================================
platform darwin -- Python 3.8.5, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/yoo/work/yuanmahui/python/ch2-requests
collected 3 items

test_sample.py 401
application/json; charset=utf-8
utf-8
{"message":"Requires authentication","documentation_url":"https://docs.github.com/rest/reference/users#get-the-authenticated-user"}
{'message': 'Requires authentication', 'documentation_url': 'https://docs.github.com/rest/reference/users#get-the-authenticated-user'}
.{"name": "game404", "age": 2}
{
  "age": 2,
  "name": "game404"
}
.game404
.

================================================== 3 passed in 1.89s ===================================================
```
可以使用下面命令测试单个函数:
```
pytest test_sample.py::test_json_pretty_print
```