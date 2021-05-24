import requests
import time

start_time = time.time()

for number in range(1, 151):
    url = f'https://www.baidu.com?q={number}'
    resp = requests.get(url)
    # pokemon = resp.json()
    print(number)

print("--- %s seconds ---" % (time.time() - start_time))