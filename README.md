# 懂球网比赛数据爬虫

> 一个基于Python的爬虫工具，用于采集懂球网单场比赛的详细数据

---

## 📋 项目简介

本项目是一个专业的体育数据采集工具，专注于从懂球网（dongqiudi.com）采集NBA比赛数据。通过调用官方API接口，获取比赛基本信息、双方交锋历史、球队近期战绩等数据，并支持多格式输出。

### 🎯 目标功能

- 采集单场比赛的基本信息（主队、客队、比分、日期）
- 获取双方球队的交锋历史记录
- 收集主队和客队的近期战绩
- 数据清洗与去重处理
- 支持Excel和CSV双格式输出

---

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| 🚀 **高效采集** | 直接调用API接口，避免复杂的HTML解析 |
| 🧹 **数据清洗** | 自动过滤无效数据，去除重复记录 |
| 📊 **多格式输出** | 支持Excel（多工作表）和CSV格式 |
| 🛡️ **请求伪装** | 设置合理的请求头，避免被拦截 |
| 📁 **结构化数据** | 清晰的数据结构，便于后续分析 |

---

## 🛠️ 技术栈

- **Python 3.8+** - 编程语言
- **requests** - HTTP请求库
- **BeautifulSoup** - HTML解析（备用）
- **pandas** - 数据处理与输出
- **openpyxl** - Excel文件处理

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Git（用于版本控制）

### 安装依赖

```bash
# 安装所需依赖包
pip install requests pandas beautifulsoup4 openpyxl
```

### 运行爬虫

```bash
# 进入项目目录
cd dongqiudi-spider

# 运行爬虫
python spider.py
```

### 输出文件

运行成功后，将生成以下文件：

| 文件 | 说明 |
|------|------|
| `match_{match_id}.xlsx` | Excel文件（含4个工作表） |
| `basic.csv` | 比赛基本信息 |
| `head_to_head.csv` | 双方交锋历史 |
| `home_recent.csv` | 主队近期战绩 |
| `away_recent.csv` | 客队近期战绩 |

---

## 📁 项目结构

```
dongqiudi-spider/
├── spider.py              # 主爬虫程序
├── data_analysis.py       # 数据分析脚本
├── md_to_docx.py          # Markdown转Word工具
├── README.md              # 项目说明文档
├── experiment_report.md   # 实验报告
├── analysis_report.md     # 数据分析报告
└── output/                # 输出数据目录
    ├── match_54452819.xlsx
    ├── basic.csv
    ├── head_to_head.csv
    ├── home_recent.csv
    └── away_recent.csv
```

---

## 🔧 配置说明

### 修改比赛ID

在 `spider.py` 中修改目标比赛ID：

```python
if __name__ == '__main__':
    match_id = '54452819'  # 修改为目标比赛ID
    main(match_id)
```

### 请求头配置

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': f'https://pc.dongqiudi.com/match/{match_id}',
    'Accept': 'application/json, text/plain, */*'
}
```

---

## 📊 使用示例

### 示例1：采集比赛数据

```bash
python spider.py
```

输出：
```
开始采集比赛ID: 54452819 的数据...
正在从API获取数据...
成功获取API数据
正在解析比赛基本信息...
基本信息: {'比赛ID': '54452819', '主队': '克利夫兰骑士', '客队': '底特律活塞', ...}
正在解析交锋历史...
交锋历史记录数: 18
正在解析主队近期战绩...
主队近期战绩记录数: 29
正在解析客队近期战绩...
客队近期战绩记录数: 30
Excel文件 match_54452819.xlsx 已保存成功
CSV文件 basic.csv 已保存成功
CSV文件 head_to_head.csv 已保存成功
CSV文件 home_recent.csv 已保存成功
CSV文件 away_recent.csv 已保存成功
数据采集完成！
```

### 示例2：数据分析

```bash
python data_analysis.py
```

输出：
```
分析报告 (Markdown) 已保存: analysis_report.md
分析报告 (Word) 已保存: analysis_report.docx
```

---

## 📝 API接口说明

### 核心接口

```
GET https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}
```

### 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `team_A` | string | 主队名称 |
| `team_B` | string | 客队名称 |
| `start_time` | string | 比赛时间 |
| `battle_history` | dict | 交锋历史数据 |
| `recent_record` | dict | 近期战绩数据 |

---

## 🐛 常见问题

### Q1: 爬虫被拦截怎么办？

**A**: 检查请求头配置，确保User-Agent和Referer设置正确。

### Q2: 比分数据为空？

**A**: 比赛可能尚未结束或数据未更新，请稍后重试。

### Q3: Excel文件无法打开？

**A**: 确保已安装`openpyxl`库：`pip install openpyxl`

---

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关网站的使用条款。

---

## 📬 联系方式

如有问题或建议，欢迎提交Issue或Pull Request。

---

**项目版本**: v1.0  
**创建日期**: 2026年  
**作者**: Sports Data Team