import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/overview/match/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

print("=== statistics ===")
statistics = data.get('statistics', {})
for key, value in statistics.items():
    print(f"\n{key}:")
    if isinstance(value, dict):
        for k, v in value.items():
            print(f"  {k}: {v}")
    elif isinstance(value, list):
        print(f"  列表长度: {len(value)}")
        if len(value) > 0:
            print(f"  第一个元素: {value[0]}")
