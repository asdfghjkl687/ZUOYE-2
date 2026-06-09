import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

print("=== 基本信息 ===")
print(f"team_A: {data.get('team_A')}")
print(f"team_B: {data.get('team_B')}")
print(f"start_time: {data.get('start_time')}")

print("\n=== battle_history ===")
battle_history = data.get('battle_history', {})
print(f"类型: {type(battle_history)}")
print(f"键: {list(battle_history.keys()) if isinstance(battle_history, dict) else '不是字典'}")

if isinstance(battle_history, dict):
    for key, value in battle_history.items():
        print(f"\n  键 '{key}' 的值类型: {type(value)}")
        if isinstance(value, list) and len(value) > 0:
            print(f"  第一个元素: {value[0]}")

print("\n=== recent_record ===")
recent_record = data.get('recent_record', {})
print(f"类型: {type(recent_record)}")
print(f"键: {list(recent_record.keys())}")

if 'team_A' in recent_record:
    team_A_records = recent_record['team_A']
    print(f"\nteam_A 记录数: {len(team_A_records)}")
    if len(team_A_records) > 0:
        print(f"第一个记录: {team_A_records[0]}")
