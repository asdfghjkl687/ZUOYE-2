import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# 下载JS文件来分析
js_urls = [
    'https://pc.dongqiudi.com/_nuxt/e4636f088ed47b4f9d74.js',
    'https://pc.dongqiudi.com/_nuxt/eabb67feb9f2b82745b6.js',
    'https://pc.dongqiudi.com/_nuxt/5699dde553d60e4ad991.js'
]

for js_url in js_urls:
    print(f'\n分析文件: {js_url}')
    try:
        r = requests.get(js_url, headers=headers)
        print(f'文件长度: {len(r.text)}')
        
        # 搜索API相关的模式
        api_patterns = [r'/api/', r'get\(', r'fetch\(', r'axios']
        for pattern in api_patterns:
            matches = re.findall(pattern, r.text)
            if matches:
                print(f'{pattern}: 找到 {len(matches)} 个匹配')
        
        # 搜索URL模式
        urls = re.findall(r'https?://[^\s"\']+', r.text)
        if urls:
            print('找到的URL:', urls[:3])
            
    except Exception as e:
        print(f'下载失败: {e}')
