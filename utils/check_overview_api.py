import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/overview/match/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

print("=== Overview API ===")
print(f"状态码: {r.status_code}")
print(f"所有键: {list(data.keys())}")

# 查看详细信息
for key in data.keys():
    value = data[key]
    if isinstance(value, dict):
        print(f"\n{key}:")
        print(f"  子键: {list(value.keys())[:10]}")
    elif isinstance(value, list):
        print(f"\n{key}: 列表，长度 {len(value)}")
        if len(value) > 0 and isinstance(value[0], dict):
            print(f"  第一个元素键: {list(value[0].keys())[:5]}")
    else:
        print(f"\n{key}: {value}")
