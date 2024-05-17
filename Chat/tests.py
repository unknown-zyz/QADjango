import requests
content = "在Linux中，命令 tail -f /dev/null 是用来查看文件内容变化的工具 tail 的一种用法。"
url = '127.0.0.1:8081/chat/'
res = requests.post(url, json={"content": content})
print(res.json()['content'])
