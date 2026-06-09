import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'

# 尝试不同的API端点
api_urls = [
    f'https://pc.dongqiudi.com/api/data/overview/match/{match_id}',
    f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}',
    f'https://pc.dongqiudi.com/api/data/match/{match_id}'
]

for url in api_urls:
    print(f'\n尝试: {url}')
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f'状态码: {r.status_code}')
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            print(f'Content-Type: {content_type}')
            
            if 'application/json' in content_type or 'text/json' in content_type:
                data = r.json()
                print(f'数据类型: {type(data)}')
                if isinstance(data, dict):
                    print(f'键: {list(data.keys())[:10]}')
                    # 查看部分数据
                    print('数据预览:')
                    for key, value in list(data.items())[:3]:
                        if isinstance(value, dict):
                            print(f'  {key}: {list(value.keys())[:5]}')
                        elif isinstance(value, list):
                            print(f'  {key}: 列表，长度 {len(value)}')
                        else:
                            print(f'  {key}: {str(value)[:50]}')
            else:
                print(f'前500字符: {r.text[:500]}')
    except Exception as e:
        print(f'错误: {e}')
