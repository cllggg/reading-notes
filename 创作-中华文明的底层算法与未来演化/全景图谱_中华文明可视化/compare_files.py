import json

with open('dynasty_data_enhanced.json', 'r', encoding='utf-8') as f1, open('dynasty_data_complete.json', 'r', encoding='utf-8') as f2:
    d1 = json.load(f1)
    d2 = json.load(f2)
    print('数据相同:', d1 == d2)
    if d1 != d2:
        print('增强数据数量:', len(d1))
        print('完整数据数量:', len(d2))
