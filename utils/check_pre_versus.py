import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

print("=== pre_versus ===")
pre_versus = data.get('pre_versus', [])
print(f"长度: {len(pre_versus)}")
for i, item in enumerate(pre_versus):
    print(f"\n第{i+1}个元素:")
    print(f"  类型: {type(item)}")
    if isinstance(item, dict):
        print(f"  键: {list(item.keys())}")
        for key, value in item.items():
            print(f"  {key}: {value}")
    else:
        print(f"  值: {item}")
