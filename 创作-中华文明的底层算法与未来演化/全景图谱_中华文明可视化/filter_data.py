import json

# 主要王朝ID列表（不包含史前文化）
main_dynasty_ids = [
    'xia', 'shang', 'chu', 'zhou_west',
    'chunqiu_zhanguo', 'qin', 'han_west', 'han_east',
    'three_kingdoms', 'sui', 'tang', 'song',
    'yuan', 'ming', 'qing'
]

# 读取完整数据
with open('dynasty_data_complete.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# 筛选主要王朝
basic_data = [item for item in all_data if item['id'] in main_dynasty_ids]

# 保存基础数据
with open('dynasty_data.json', 'w', encoding='utf-8') as f:
    json.dump(basic_data, f, ensure_ascii=False, indent=2)

print(f"基础数据已保存，包含 {len(basic_data)} 个主要王朝")
