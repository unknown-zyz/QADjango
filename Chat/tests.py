import requests

url = f'http://172.16.26.4:8081/chats/3/'
ret = requests.post(url, json={"content": "怎样维护cessna-172-amm？"}).json()['message']['content']
print(ret)

