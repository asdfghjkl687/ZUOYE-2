import requests
import re

url = 'https://pc.dongqiudi.com/match/54452819'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

r = requests.get(url, headers=headers)
text = r.text

# 查找所有引用的JS文件
js_files = re.findall(r'<script[^>]*src="([^"]+)"', text)
print('引用的JS文件:')
for js in js_files:
    print(js)

print('\n' + '='*50 + '\n')

# 搜索页面中的数字和可能的API模式
api_patterns = [
    r'/match/\d+',
    r'/api/',
    r'data-'
]

print('页面中找到的模式:')
for pattern in api_patterns:
    matches = re.findall(pattern, text)
    if matches:
        print(f'{pattern}: {matches[:5]}')

print('\n' + '='*50 + '\n')

# 查看页面中的关键部分
print('页面长度:', len(text))
print('是否包含表格:', '<table' in text)
print('是否包含team:', 'team' in text.lower())
print('是否包含score:', 'score' in text.lower())
