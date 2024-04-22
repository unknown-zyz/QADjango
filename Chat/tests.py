import json

# 将 Python 对象转换为 JSON 格式的字符串
data = ['name', 'John', 'age', 30]
json_string = json.dumps(data)
print(json_string)

# 将 JSON 格式的字符串转换为 Python 对象
parsed_data = json.loads(json_string)
print(parsed_data)
print(parsed_data[0])
