<<<<<<< HEAD
# 懂球网数据采集系统

## 项目简介

本项目是一个专业的体育数据爬虫系统，专注于从懂球网采集NBA比赛的详细数据。系统通过直接调用懂球网API接口，高效、稳定地获取比赛基本信息、双方交锋历史、球队近期战绩等核心数据，并支持多种格式输出，为体育数据分析提供可靠的数据源。

### 核心功能

- 🏀 **比赛数据采集**：采集单场比赛的完整信息
- 📊 **交锋历史分析**：获取两队历史交锋记录
- 📈 **近期战绩追踪**：追踪主客队近期比赛表现
- 🧹 **数据清洗处理**：自动去重、格式统一、数据过滤
- 📄 **多格式输出**：支持Excel和CSV双格式输出

---

## 功能特性

### 1. 智能数据采集
- 通过API接口直接获取结构化数据
- 自动识别并解析JSON数据结构
- 支持批量采集多场比赛数据

### 2. 完善的数据处理
- 自动过滤不完整和无效数据
- 智能去重算法，避免重复记录
- 统一比分格式（如：112-103）

### 3. 多格式输出支持
- **Excel格式**：多工作表输出，便于数据管理
- **CSV格式**：独立文件输出，便于数据导入分析

### 4. 数据分析功能
- 双方交锋历史分析
- 主客队近期战绩对比
- 胜率、得分等关键指标统计
- 自动生成可视化图表

### 5. 完整的文档支持
- 详细的实验报告
- 数据分析报告
- 爬虫实现流程文档
- 代码注释完善

---

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.13+ | 主要开发语言 |
| requests | - | HTTP请求库 |
| pandas | - | 数据处理与分析 |
| beautifulsoup4 | - | HTML解析（备用） |
| openpyxl | - | Excel文件操作 |
| python-docx | - | Word文档生成 |

---

## 项目结构

```
懂球网数据采集系统/
├── spider.py                    # 主爬虫程序
├── data_analysis.py             # 数据分析脚本
├── md_to_docx.py                # Markdown转Word工具
├── README.md                    # 项目说明文档
├── requirements.txt             # 依赖包列表
├── output.log                   # 运行日志
├── docs/                        # 文档目录
│   ├── experiment_report.md     # 实验报告
│   ├── analysis_report.md       # 数据分析报告
│   └── spider_flow.md           # 爬虫实现流程
├── data/                        # 数据输出目录
│   ├── match_54452819.xlsx      # Excel数据文件
│   ├── basic.csv                # 基本信息
│   ├── head_to_head.csv         # 交锋历史
│   ├── home_recent.csv          # 主队近期战绩
│   └── away_recent.csv          # 客队近期战绩
└── utils/                       # 工具脚本
    ├── analyze_js.py            # JavaScript分析
    ├── find_api.py              # API接口查找
    └── test_api.py              # API测试工具
```

---

## 快速开始

### 环境要求

- Python 3.13 或更高版本
- pip 包管理器
- 网络连接（访问懂球网API）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/asdfghjkl687/ZUOYE-2.git
cd ZUOYE-2/懂球网数据采集系统
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests pandas beautifulsoup4 openpyxl python-docx
```

#### 3. 配置参数

编辑 `spider.py` 文件，修改比赛ID：

```python
# 设置要采集的比赛ID
MATCH_ID = '54452819'
```

#### 4. 运行爬虫

```bash
# 采集比赛数据
python spider.py

# 运行数据分析
python data_analysis.py
```

---

## 使用说明

### 采集单场比赛数据

```bash
python spider.py
```

**输出文件**：
- `match_{match_id}.xlsx` - 完整比赛数据（Excel格式）
- `basic.csv` - 比赛基本信息
- `head_to_head.csv` - 双方交锋历史
- `home_recent.csv` - 主队近期战绩
- `away_recent.csv` - 客队近期战绩

### 运行数据分析

```bash
python data_analysis.py
```

**输出文件**：
- `analysis_report.md` - 数据分析报告（Markdown格式）
- `analysis_report.docx` - 数据分析报告（Word格式）

### 转换文档格式

```bash
python md_to_docx.py input.md output.docx
```

---

## 配置说明

### 请求头配置

在 `spider.py` 中可以自定义请求头：

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': f'https://pc.dongqiudi.com/match/{match_id}',
    'Accept': 'application/json, text/plain, */*'
}
```

### API接口配置

默认使用懂球网API接口：

```python
api_url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'
```

### 输出路径配置

修改输出文件路径：

```python
output_dir = 'data/'  # 数据输出目录
```

---

## 部署说明

### 本地部署

1. **环境准备**
   ```bash
   # 创建虚拟环境（推荐）
   python -m venv venv
   
   # 激活虚拟环境
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python spider.py
   ```

### 服务器部署

1. **上传项目到服务器**
   ```bash
   scp -r 懂球网数据采集系统 user@server:/path/to/project
   ```

2. **配置定时任务（Cron）**
   ```bash
   # 编辑crontab
   crontab -e
   
   # 添加定时任务（每天凌晨2点运行）
   0 2 * * * cd /path/to/project && python spider.py >> output.log 2>&1
   ```

3. **使用Docker部署（可选）**

   创建 `Dockerfile`：
   ```dockerfile
   FROM python:3.13-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   CMD ["python", "spider.py"]
   ```

   构建并运行：
   ```bash
   docker build -t dongqiudi-spider .
   docker run -v $(pwd)/data:/app/data dongqiudi-spider
   ```

---

## 常见问题

### 1. 比分数据缺失怎么办？

**原因**：比赛尚未开始或数据未更新到API

**解决方案**：
- 等待比赛结束后重新运行脚本
- 检查比赛ID是否正确
- 查看懂球网页面确认数据是否可用

### 2. 网络请求失败怎么办？

**原因**：网络连接问题或API接口限制

**解决方案**：
- 检查网络连接
- 增加请求超时时间
- 更换User-Agent
- 添加请求间隔，避免频繁请求

### 3. 如何采集多场比赛？

**解决方案**：修改 `spider.py`，循环采集多个比赛ID：

```python
match_ids = ['54452819', '54452820', '54452821']
for match_id in match_ids:
    get_match_data(match_id)
    time.sleep(2)  # 添加请求间隔
```

### 4. 如何自定义输出格式？

**解决方案**：修改 `save_to_excel()` 和 `save_to_csv()` 函数，自定义字段和格式。

---

## 项目文档

- [实验报告](docs/experiment_report.md) - 详细的实验过程和结果
- [数据分析报告](docs/analysis_report.md) - 比赛数据深度分析
- [爬虫实现流程](docs/spider_flow.md) - 技术实现详解

---

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- 项目地址：[https://github.com/asdfghjkl687/ZUOYE-2](https://github.com/asdfghjkl687/ZUOYE-2)
- 问题反馈：[Issues](https://github.com/asdfghjkl687/ZUOYE-2/issues)

---

## 更新日志

### v1.0.0 (2026-05-16)
- ✨ 初始版本发布
- 🎯 实现基础数据采集功能
- 📊 支持Excel和CSV双格式输出
- 📈 添加数据分析功能
- 📝 完善项目文档

---

## 致谢

感谢懂球网提供的数据接口，本项目仅用于学习和研究目的，请勿用于商业用途。

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**
