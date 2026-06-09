#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
懂球网单场比赛数据采集爬虫

功能：
1. 采集比赛基本信息（主队、客队、比分、日期）
2. 采集双方交锋历史
3. 采集主队近期战绩
4. 采集客队近期战绩
5. 数据清洗与去重
6. 输出Excel和CSV文件
"""

import requests
import pandas as pd
import re
from datetime import datetime
import json

def get_match_data(match_id):
    """
    从API获取比赛数据
    
    Args:
        match_id (str): 比赛ID
        
    Returns:
        dict: 包含比赛数据的字典，如果失败返回空字典
    """
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': f'https://pc.dongqiudi.com/match/{match_id}',
        'Connection': 'keep-alive'
    }
    
    # API端点
    api_url = f'https://pc.dongqiudi.com/api/data/match/pre_analysis_v1/{match_id}'
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取API数据失败: {e}")
        return {}

def parse_basic_info(api_data, match_id):
    """
    解析比赛基本信息
    
    Args:
        api_data (dict): API返回的数据
        match_id (str): 比赛ID
        
    Returns:
        dict: 包含比赛基本信息的字典
    """
    basic_info = {
        '比赛ID': match_id,
        '主队': api_data.get('team_A', ''),
        '客队': api_data.get('team_B', ''),
        '比分': '',
        '日期': ''
    }
    
    # 从start_time提取日期
    start_time = api_data.get('start_time', '')
    if start_time:
        # 格式: 2026-05-12 00:00:00
        date_str = start_time.split(' ')[0]
        basic_info['日期'] = date_str
    
    # 尝试从交锋历史中获取本场比赛的比分
    battle_history = api_data.get('battle_history', {})
    if battle_history:
        # 交锋历史数据在 'list' 键中
        history_list = battle_history.get('list', [])
        if history_list:
            # 查找日期匹配的比赛
            for record in history_list:
                record_date = record.get('date', '')
                record_year = record.get('year', '')
                if record_date and record_year:
                    # 构建完整日期进行比较
                    record_full_date = f"{record_year}-{record_date}"
                    if record_full_date == basic_info['日期']:
                        basic_info['比分'] = record.get('score', '')
                        break
    
    # 如果没找到比分，尝试从主队近期战绩中获取
    if not basic_info['比分']:
        team_A_records = api_data.get('recent_record', {}).get('team_A', [])
        for record in team_A_records:
            record_date = record.get('date', '')
            record_year = record.get('year', '')
            if record_date and record_year:
                record_full_date = f"{record_year}-{record_date}"
                if record_full_date == basic_info['日期']:
                    basic_info['比分'] = record.get('score', '')
                    break
    
    # 如果没找到比分，尝试从客队近期战绩中获取
    if not basic_info['比分']:
        team_B_records = api_data.get('recent_record', {}).get('team_B', [])
        for record in team_B_records:
            record_date = record.get('date', '')
            record_year = record.get('year', '')
            if record_date and record_year:
                record_full_date = f"{record_year}-{record_date}"
                if record_full_date == basic_info['日期']:
                    basic_info['比分'] = record.get('score', '')
                    break
    
    # 如果还是没找到比分，输出提示信息
    if not basic_info['比分']:
        print(f"警告: 未找到比赛 {basic_info['日期']} 的比分数据")
    
    # 统一比分格式为"112-103"
    if basic_info['比分']:
        basic_info['比分'] = re.sub(r'\s*[:-]\s*', '-', basic_info['比分'])
    
    return basic_info

def parse_battle_history(api_data):
    """
    解析双方交锋历史
    
    Args:
        api_data (dict): API返回的数据
        
    Returns:
        list: 包含交锋历史记录的列表
    """
    battle_history = []
    
    # 获取交锋历史数据（数据在 'list' 键中）
    history_data = api_data.get('battle_history', {})
    if not history_data:
        return battle_history
    
    records = history_data.get('list', [])
    for record in records:
        if isinstance(record, dict):
            row = {
                '赛事': record.get('competition', ''),
                '日期': f"{record.get('year', '')}-{record.get('date', '')}" if record.get('year') and record.get('date') else '',
                '主队': record.get('team_A_name', ''),
                '比分': re.sub(r'\s*[:-]\s*', '-', record.get('score', '')),
                '客队': record.get('team_B_name', '')
            }
            battle_history.append(row)
    
    return battle_history

def parse_recent_record(api_data, team_type='team_A'):
    """
    解析球队近期战绩
    
    Args:
        api_data (dict): API返回的数据
        team_type (str): 'team_A' 表示主队，'team_B' 表示客队
        
    Returns:
        list: 包含近期战绩记录的列表
    """
    recent_record = []
    
    # 获取近期战绩数据
    records = api_data.get('recent_record', {})
    team_records = records.get(team_type, [])
    
    for record in team_records:
        if isinstance(record, dict):
            row = {
                '赛事': record.get('competition', ''),
                '日期': f"{record.get('year', '')}-{record.get('date', '')}" if record.get('year') and record.get('date') else '',
                '主队': record.get('team_A_name', ''),
                '比分': re.sub(r'\s*[:-]\s*', '-', record.get('score', '')),
                '客队': record.get('team_B_name', '')
            }
            recent_record.append(row)
    
    return recent_record

def clean_data(data_list):
    """
    清洗数据，去重并过滤不完整的行
    
    Args:
        data_list (list): 原始数据列表
        
    Returns:
        list: 清洗后的数据列表
    """
    cleaned = []
    seen = set()  # 用于去重的集合
    
    for row in data_list:
        # 跳过不完整的行（日期或比分为空）
        if not row.get('日期') or not row.get('比分'):
            continue
        
        # 跳过比分全是"-"的未开始比赛
        if row['比分'] == '-' or row['比分'] == '--':
            continue
        
        # 跳过比分不包含数字的行
        if not re.search(r'\d+', row['比分']):
            continue
        
        # 跳过日期格式不正确的行
        if not re.match(r'\d{4}-\d{2}-\d{2}', row['日期']):
            continue
        
        # 生成去重键（日期+主队+客队+比分）
        unique_key = (row['日期'], row['主队'], row['客队'], row['比分'])
        
        if unique_key not in seen:
            seen.add(unique_key)
            cleaned.append(row)
    
    return cleaned

def save_to_excel(data_dict, filename):
    """
    将数据保存到Excel文件（多工作表）
    
    Args:
        data_dict (dict): 包含各工作表数据的字典
        filename (str): 输出文件名
    """
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, data in data_dict.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Excel文件 {filename} 已保存成功")
    except Exception as e:
        print(f"保存Excel文件失败: {e}")

def save_to_csv(data_dict, base_filename):
    """
    将数据保存到CSV文件（每个工作表一个文件）
    
    Args:
        data_dict (dict): 包含各工作表数据的字典
        base_filename (str): 基础文件名（不含扩展名）
    """
    csv_filenames = {
        '本场基本信息': 'basic.csv',
        '交锋历史': 'head_to_head.csv',
        '主队近期战绩': 'home_recent.csv',
        '客队近期战绩': 'away_recent.csv'
    }
    
    try:
        for sheet_name, data in data_dict.items():
            csv_filename = csv_filenames.get(sheet_name, f"{sheet_name}.csv")
            df = pd.DataFrame(data)
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"CSV文件 {csv_filename} 已保存成功")
    except Exception as e:
        print(f"保存CSV文件失败: {e}")

def main():
    """
    主函数：执行完整的爬虫流程
    """
    # 目标URL
    url = 'https://pc.dongqiudi.com/match/54452819'
    
    # 从URL中提取比赛ID
    match_id = re.search(r'/match/(\d+)', url).group(1) if re.search(r'/match/(\d+)', url) else 'unknown'
    
    print(f"开始采集比赛ID: {match_id} 的数据...")
    
    # 1. 从API获取数据
    print("正在从API获取数据...")
    api_data = get_match_data(match_id)
    
    if not api_data:
        print("无法获取数据，程序退出")
        return
    
    print("成功获取API数据")
    
    # 2. 解析比赛基本信息
    print("正在解析比赛基本信息...")
    basic_info = parse_basic_info(api_data, match_id)
    print(f"基本信息: {basic_info}")
    
    # 3. 解析交锋历史
    print("正在解析交锋历史...")
    head_to_head_data = parse_battle_history(api_data)
    head_to_head_data = clean_data(head_to_head_data)
    print(f"交锋历史记录数: {len(head_to_head_data)}")
    
    # 4. 解析主队近期战绩
    print("正在解析主队近期战绩...")
    home_recent_data = parse_recent_record(api_data, 'team_A')
    home_recent_data = clean_data(home_recent_data)
    print(f"主队近期战绩记录数: {len(home_recent_data)}")
    
    # 5. 解析客队近期战绩
    print("正在解析客队近期战绩...")
    away_recent_data = parse_recent_record(api_data, 'team_B')
    away_recent_data = clean_data(away_recent_data)
    print(f"客队近期战绩记录数: {len(away_recent_data)}")
    
    # 6. 准备输出数据
    output_data = {
        '本场基本信息': [basic_info],
        '交锋历史': head_to_head_data,
        '主队近期战绩': home_recent_data,
        '客队近期战绩': away_recent_data
    }
    
    # 7. 保存为Excel文件
    excel_filename = f'match_{match_id}.xlsx'
    save_to_excel(output_data, excel_filename)
    
    # 8. 保存为CSV文件
    save_to_csv(output_data, f'match_{match_id}')
    
    print("\n数据采集完成！")
    print(f"比赛ID: {match_id}")
    print(f"主队: {basic_info['主队']}")
    print(f"客队: {basic_info['客队']}")
    print(f"比分: {basic_info['比分']}")
    print(f"日期: {basic_info['日期']}")
    print(f"输出文件: {excel_filename}, basic.csv, head_to_head.csv, home_recent.csv, away_recent.csv")

if __name__ == '__main__':
    main()
