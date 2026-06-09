import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# 下载包含API调用的JS文件
js_url = 'https://pc.dongqiudi.com/_nuxt/5699dde553d60e4ad991.js'
r = requests.get(js_url, headers=headers)
text = r.text

# 搜索API端点模式
# 查找类似 /api/xxx 的模式
api_patterns = [
    r'/api/[a-zA-Z0-9_/]+',
    r'api\.dongqiudi\.com/[a-zA-Z0-9_/]+',
    r'pc\.dongqiudi\.com/api/[a-zA-Z0-9_/]+'
]

print("找到的API端点:")
for pattern in api_patterns:
    matches = re.findall(pattern, text)
    if matches:
        for match in set(matches):  # 去重
            print(f"  {match}")

# 搜索包含match的API
print("\n包含match的API:")
match_apis = [m for m in re.findall(r'/api/[a-zA-Z0-9_/]+', text) if 'match' in m.lower()]
for api in set(match_apis):
    print(f"  {api}")
