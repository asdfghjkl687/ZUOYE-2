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

print("=== API返回数据结构 ===")
print(f"状态码: {r.status_code}")
print(f"所有键: {list(data.keys())}")

# 打印详细信息
print("\n=== 基本信息 ===")
print(f"matchId: {data.get('matchId')}")
print(f"competition_id: {data.get('competition_id')}")
print(f"team_A (主队): {data.get('team_A')}")
print(f"team_A_href: {data.get('team_A_href')}")
print(f"team_A_logo: {data.get('team_A_logo')}")
print(f"team_B (客队): {data.get('team_B')}")
print(f"team_B_href: {data.get('team_B_href')}")
print(f"team_B_logo: {data.get('team_B_logo')}")
print(f"start_time: {data.get('start_time')}")

# 打印交锋历史
print("\n=== 交锋历史 ===")
battle_history = data.get('battle_history', [])
print(f"交锋历史记录数: {len(battle_history)}")
if battle_history:
    print("字段:", list(battle_history[0].keys()))
    for i, record in enumerate(battle_history[:5]):
        print(f"{i+1}. {record}")

# 打印主队近期战绩
print("\n=== 主队近期战绩 ===")
team_A_recent = data.get('team_A_recent', [])
print(f"主队近期战绩记录数: {len(team_A_recent)}")
if team_A_recent:
    print("字段:", list(team_A_recent[0].keys()))
    for i, record in enumerate(team_A_recent[:5]):
        print(f"{i+1}. {record}")

# 打印客队近期战绩
print("\n=== 客队近期战绩 ===")
team_B_recent = data.get('team_B_recent', [])
print(f"客队近期战绩记录数: {len(team_B_recent)}")
if team_B_recent:
    print("字段:", list(team_B_recent[0].keys()))
    for i, record in enumerate(team_B_recent[:5]):
        print(f"{i+1}. {record}")
