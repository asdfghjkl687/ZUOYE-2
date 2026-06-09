import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://pc.dongqiudi.com/match/54452819'
}

match_id = '54452819'
url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'

r = requests.get(url, headers=headers)
data = r.json()

print("=== 查找2026-05-12的比赛 ===")

# 检查主队近期战绩
team_A_records = data.get('recent_record', {}).get('team_A', [])
print(f"\n主队近期战绩 ({len(team_A_records)} 条):")
for record in team_A_records:
    date = f"{record.get('year', '')}-{record.get('date', '')}"
    if '2026-05-12' in date:
        print(f"找到: {record}")

# 检查客队近期战绩
team_B_records = data.get('recent_record', {}).get('team_B', [])
print(f"\n客队近期战绩 ({len(team_B_records)} 条):")
for record in team_B_records:
    date = f"{record.get('year', '')}-{record.get('date', '')}"
    if '2026-05-12' in date:
        print(f"找到: {record}")

# 检查交锋历史
history_list = data.get('battle_history', {}).get('list', [])
print(f"\n交锋历史 ({len(history_list)} 条):")
for record in history_list:
    date = f"{record.get('year', '')}-{record.get('date', '')}"
    if '2026-05-12' in date:
        print(f"找到: {record}")
