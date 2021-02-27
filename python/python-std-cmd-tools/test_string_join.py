
def test_normal():
	tmp = ""
	for x in range(100):
		if x % 2 == 0:
			if tmp:
				tmp = tmp+"-"+str(x)
			else:
				tmp = str(x)
	return tmp

def test_reduce():
	from functools import reduce
	return reduce((lambda x, y: str(x) +"-"+ str(y)), [n for n in range(100) if n%2 == 0])

if __name__ == '__main__':
	print(test_normal())
	# print(test_reduce())