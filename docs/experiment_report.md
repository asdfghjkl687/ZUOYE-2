# 懂球网单场比赛数据采集实验报告

## 一、实验概述

### 1.1 实验目标
本实验旨在开发一个Python爬虫程序，从懂球网采集单场NBA比赛（克利夫兰骑士 vs 底特律活塞）的详细数据，包括：
- 比赛基本信息（主队、客队、比分、日期）
- 双方交锋历史
- 主队近期战绩
- 客队近期战绩

### 1.2 实验环境
| 项目 | 说明 |
|------|------|
| 操作系统 | Windows 10 |
| Python版本 | 3.13 |
| 主要依赖 | requests, pandas, beautifulsoup4, openpyxl |
| 目标URL | https://pc.dongqiudi.com/match/54452819 |

---

## 二、技术方案

### 2.1 数据获取方式

经过分析，懂球网采用Vue.js动态渲染页面，数据通过API接口加载。通过分析JavaScript文件，发现核心API端点：

```
https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}
```

### 2.2 技术选型

| 技术 | 用途 | 选择理由 |
|------|------|----------|
| requests | HTTP请求 | 轻量级、性能好 |
| BeautifulSoup | HTML解析 | 备用方案，实际使用API |
| pandas | 数据处理 | 强大的数据处理能力 |
| openpyxl | Excel输出 | 支持多工作表输出 |

### 2.3 数据采集流程

```
请求API → 解析JSON → 数据清洗 → 去重过滤 → 输出文件
```

---

## 三、实现步骤

### 3.1 依赖安装

```bash
pip install requests pandas beautifulsoup4 openpyxl
```

### 3.2 API接口分析

通过分析懂球网前端JavaScript代码，发现数据接口结构如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `team_A` | string | 主队名称 |
| `team_B` | string | 客队名称 |
| `start_time` | string | 比赛时间 |
| `battle_history` | dict | 交锋历史（含`list`键） |
| `recent_record` | dict | 近期战绩（含`team_A`/`team_B`键） |

### 3.3 核心代码实现

#### 3.3.1 API数据获取

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

#### 3.3.2 数据清洗与去重

```python
def clean_data(data_list):
    cleaned = []
    seen = set()
    for row in data_list:
        # 过滤不完整行和未开始比赛
        if not row.get('日期') or not row.get('比分'):
            continue
        if row['比分'] == '-' or not re.search(r'\d+', row['比分']):
            continue
        # 去重
        unique_key = (row['日期'], row['主队'], row['客队'], row['比分'])
        if unique_key not in seen:
            seen.add(unique_key)
            cleaned.append(row)
    return cleaned
```

#### 3.3.3 多格式输出

```python
# Excel输出（多工作表）
with pd.ExcelWriter('match_54452819.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='本场基本信息', index=False)
    df.to_excel(writer, sheet_name='交锋历史', index=False)
    df.to_excel(writer, sheet_name='主队近期战绩', index=False)
    df.to_excel(writer, sheet_name='客队近期战绩', index=False)

# CSV输出（独立文件）
df.to_csv('basic.csv', index=False, encoding='utf-8-sig')
df.to_csv('head_to_head.csv', index=False, encoding='utf-8-sig')
df.to_csv('home_recent.csv', index=False, encoding='utf-8-sig')
df.to_csv('away_recent.csv', index=False, encoding='utf-8-sig')
```

---

## 四、实验结果

### 4.1 数据采集结果

| 数据类型 | 记录数 | 状态 |
|----------|--------|------|
| 本场基本信息 | 1条 | 成功 |
| 双方交锋历史 | 18条 | 成功 |
| 主队近期战绩 | 29条 | 成功 |
| 客队近期战绩 | 30条 | 成功 |

### 4.2 基本信息示例

```
比赛ID: 54452819
主队: 克利夫兰骑士
客队: 底特律活塞
日期: 2026-05-12
```

### 4.3 交锋历史示例

| 赛事 | 日期 | 主队 | 比分 | 客队 |
|------|------|------|------|------|
| NBA | 2026-05-09 | 克利夫兰骑士 | 116-109 | 底特律活塞 |
| NBA | 2026-05-07 | 底特律活塞 | 107-97 | 克利夫兰骑士 |
| NBA | 2026-05-05 | 底特律活塞 | 111-101 | 克利夫兰骑士 |

### 4.4 输出文件列表

```
match_54452819.xlsx  (Excel文件，含4个工作表)
basic.csv             (基本信息)
head_to_head.csv      (交锋历史)
home_recent.csv       (主队近期战绩)
away_recent.csv       (客队近期战绩)
```

---

## 五、问题与解决方案

### 5.1 问题一：页面动态渲染

**问题描述**：初始使用BeautifulSoup解析静态HTML，无法获取数据。

**解决方案**：通过分析JavaScript文件，发现API接口，改用requests直接调用API。

### 5.2 问题二：Selenium无法运行

**问题描述**：尝试使用Selenium获取动态页面失败，提示"Could not reach host"。

**解决方案**：放弃Selenium方案，专注于API接口分析，成功找到数据接口。

### 5.3 问题三：比分数据缺失

**问题描述**：本场比赛（2026-05-12）的比分在API中暂不可用。

**解决方案**：
1. 多次尝试从交锋历史、主队战绩、客队战绩中查找
2. 添加警告提示用户比分暂不可用
3. 建议用户稍后重新运行脚本获取更新数据

### 5.4 问题四：数据结构复杂

**问题描述**：API返回的数据结构嵌套较深，需要逐层解析。

**解决方案**：编写专门的解析函数，明确数据路径：
- 交锋历史：`battle_history['list']`
- 近期战绩：`recent_record['team_A']` / `recent_record['team_B']`

---

## 六、结论

### 6.1 实验成果

1. ✅ 成功开发懂球网比赛数据爬虫
2. ✅ 实现多数据源采集（API接口）
3. ✅ 完成数据清洗与去重
4. ✅ 支持Excel和CSV双格式输出
5. ✅ 代码结构清晰，注释详细

### 6.2 数据局限性

- **比分缺失**：本场比赛（2026-05-12）的比分数据暂未在API中更新
- **数据时效性**：体育数据可能随时间变化

### 6.3 后续建议

1. **定时任务**：可设置定时任务定期更新数据
2. **多比赛支持**：扩展支持批量采集多场比赛
3. **数据可视化**：结合Matplotlib进行数据分析和可视化

---

## 七、附录

### 7.1 运行方式

```bash
# 进入项目目录
cd d:\wenjian\Trae\WLPC

# 运行爬虫
python spider.py

# 检查比分更新
python check_score.py
```

### 7.2 文件说明

| 文件 | 说明 |
|------|------|
| `spider.py` | 主爬虫程序 |
| `match_54452819.xlsx` | Excel输出文件 |
| `basic.csv` | 基本信息CSV |
| `head_to_head.csv` | 交锋历史CSV |
| `home_recent.csv` | 主队战绩CSV |
| `away_recent.csv` | 客队战绩CSV |

---

**实验日期**：2026年5月13日  
**实验环境**：Windows 10 + Python 3.13