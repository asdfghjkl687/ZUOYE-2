import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

# 打印交锋历史
print("=== 交锋历史 ===")
battle_history = data.get('battle_history', {})
print(f"类型: {type(battle_history)}")
print(f"内容: {battle_history}")

# 打印近期战绩
print("\n=== 近期战绩 ===")
recent_record = data.get('recent_record', {})
print(f"类型: {type(recent_record)}")
print(f"键: {list(recent_record.keys())}")

# 查看pre_versus
print("\n=== pre_versus ===")
pre_versus = data.get('pre_versus', {})
print(f"类型: {type(pre_versus)}")
if isinstance(pre_versus, dict):
    print(f"键: {list(pre_versus.keys())}")
