# 懂球网爬虫实现流程文档

## 一、需求分析

### 1.1 目标
采集懂球网单场比赛的详细数据

### 1.2 数据需求
- 本场基本信息：主队名称、客队名称、全场比分、比赛日期
- 双方交锋历史：赛事、日期、主队、比分、客队
- 主队近期战绩：赛事、日期、主队、比分、客队、胜率
- 客队近期战绩：赛事、日期、主队、比分、客队、胜率

### 1.3 输出要求
- Excel文件（多工作表）
- CSV文件（独立文件）

---

## 二、技术方案

### 2.1 技术选型

| 技术 | 用途 | 选择理由 |
|------|------|----------|
| requests | HTTP请求 | 轻量级、性能好 |
| BeautifulSoup | HTML解析 | 备用方案 |
| pandas | 数据处理 | 强大的数据处理能力 |
| openpyxl | Excel输出 | 支持多工作表输出 |

### 2.2 数据获取方式
通过分析懂球网前端JavaScript代码，发现API接口：
```
https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}
```

---

## 三、实现流程

### 3.1 流程概述

```
请求API → 解析JSON → 数据清洗 → 去重过滤 → 输出文件
```

### 3.2 详细步骤

#### 步骤1：发送HTTP请求
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': f'https://pc.dongqiudi.com/match/{match_id}'
}
response = requests.get(api_url, headers=headers)
```

#### 步骤2：解析JSON数据
```python
data = response.json()
team_A = data.get('team_A', '')      # 主队名称
team_B = data.get('team_B', '')      # 客队名称
start_time = data.get('start_time', '')  # 比赛时间
```

#### 步骤3：提取交锋历史
```python
battle_history = data.get('battle_history', {}).get('list', [])
for record in battle_history:
    row = {
        '赛事': record.get('competition', ''),
        '日期': f"{record.get('year', '')}-{record.get('date', '')}",
        '主队': record.get('team_A_name', ''),
        '比分': record.get('score', ''),
        '客队': record.get('team_B_name', '')
    }
```

#### 步骤4：提取近期战绩
```python
team_A_records = data.get('recent_record', {}).get('team_A', [])
team_B_records = data.get('recent_record', {}).get('team_B', [])
```

#### 步骤5：数据清洗
```python
# 过滤不完整行
if not row.get('日期') or not row.get('比分'):
    continue

# 统一比分格式
row['比分'] = re.sub(r'\s*[:-]\s*', '-', row['比分'])
```

#### 步骤6：去重处理
```python
seen = set()
unique_key = (row['日期'], row['主队'], row['客队'], row['比分'])
if unique_key not in seen:
    seen.add(unique_key)
    cleaned.append(row)
```

#### 步骤7：输出文件
```python
# Excel输出
with pd.ExcelWriter('match_54452819.xlsx') as writer:
    df.to_excel(writer, sheet_name='本场基本信息', index=False)
    df.to_excel(writer, sheet_name='交锋历史', index=False)
    df.to_excel(writer, sheet_name='主队近期战绩', index=False)
    df.to_excel(writer, sheet_name='客队近期战绩', index=False)

# CSV输出
df.to_csv('basic.csv', index=False, encoding='utf-8-sig')
```

---

## 四、数据结构

### 4.1 API返回结构

| 字段 | 类型 | 说明 |
|------|------|------|
| team_A | string | 主队名称 |
| team_B | string | 客队名称 |
| start_time | string | 比赛时间 |
| battle_history | dict | 交锋历史数据 |
| recent_record | dict | 近期战绩数据 |

### 4.2 输出数据格式

| 数据类型 | 字段 |
|----------|------|
| 基本信息 | 比赛ID、主队、客队、比分、日期 |
| 交锋历史 | 赛事、日期、主队、比分、客队 |
| 近期战绩 | 赛事、日期、主队、比分、客队 |

---

## 五、核心代码模块

### 5.1 数据获取模块
```python
def get_match_data(match_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://pc.dongqiudi.com/match/{match_id}'
    }
    api_url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'
    response = requests.get(api_url, headers=headers, timeout=30)
    return response.json()
```

### 5.2 数据解析模块
```python
def parse_basic_info(api_data, match_id):
    basic_info = {
        '比赛ID': match_id,
        '主队': api_data.get('team_A', ''),
        '客队': api_data.get('team_B', ''),
        '比分': '',
        '日期': ''
    }
    start_time = api_data.get('start_time', '')
    if start_time:
        basic_info['日期'] = start_time.split(' ')[0]
    return basic_info
```

### 5.3 数据清洗模块
```python
def clean_data(data_list):
    cleaned = []
    seen = set()
    for row in data_list:
        if not row.get('日期') or not row.get('比分'):
            continue
        if row['比分'] == '-' or not re.search(r'\d+', row['比分']):
            continue
        unique_key = (row['日期'], row['主队'], row['客队'], row['比分'])
        if unique_key not in seen:
            seen.add(unique_key)
            cleaned.append(row)
    return cleaned
```

### 5.4 文件输出模块
```python
def save_to_excel(basic_info, battle_history, home_recent, away_recent, match_id):
    with pd.ExcelWriter(f'match_{match_id}.xlsx') as writer:
        pd.DataFrame([basic_info]).to_excel(writer, sheet_name='本场基本信息', index=False)
        pd.DataFrame(battle_history).to_excel(writer, sheet_name='交锋历史', index=False)
        pd.DataFrame(home_recent).to_excel(writer, sheet_name='主队近期战绩', index=False)
        pd.DataFrame(away_recent).to_excel(writer, sheet_name='客队近期战绩', index=False)
```

---

## 六、运行方式

### 6.1 依赖安装
```bash
pip install requests pandas beautifulsoup4 openpyxl
```

### 6.2 运行爬虫
```bash
python spider.py
```

### 6.3 输出文件
```
match_54452819.xlsx  # Excel文件
basic.csv             # 基本信息
head_to_head.csv      # 交锋历史
home_recent.csv       # 主队近期战绩
away_recent.csv       # 客队近期战绩
```

---

## 七、问题与解决方案

### 7.1 问题：页面动态渲染
- 现象：静态HTML不含数据
- 解决方案：分析JavaScript，找到API接口

### 7.2 问题：Selenium无法运行
- 现象：提示"Could not reach host"
- 解决方案：放弃Selenium，直接调用API

### 7.3 问题：比分数据缺失
- 现象：本场比赛比分暂不可用
- 解决方案：提示用户稍后重新运行

### 7.4 问题：数据结构复杂
- 现象：JSON嵌套较深
- 解决方案：编写专门的解析函数

---

## 八、总结

### 8.1 实现成果
- ✅ 成功采集比赛基本信息
- ✅ 成功采集交锋历史数据
- ✅ 成功采集近期战绩数据
- ✅ 数据清洗与去重
- ✅ 多格式输出支持

### 8.2 技术亮点
- 直接调用API接口，避免HTML解析复杂性
- 完善的数据清洗和去重机制
- 支持Excel和CSV双格式输出
- 代码结构清晰，易于维护

---

**文档版本**：1.0  
**创建日期**：2026年5月16日  
**文件路径**：d:\wenjian\Trae\WLPC