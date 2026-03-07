#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除JSON中不存在的图片引用
"""

import json
from pathlib import Path

JSON_FILE = Path(__file__).parent.parent / "dynasty_data_enhanced.json"
IMAGE_DIR = Path(__file__).parent

# 读取JSON文件
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取已下载的图片列表
downloaded_images = set([f.name for f in IMAGE_DIR.glob("*.jpg")])

# 移除不存在的图片引用
removed_count = 0
kept_count = 0

for dynasty in data:
    if 'events' in dynasty:
        for event in dynasty['events']:
            if 'image' in event:
                image_filename = event['image'].split('/')[-1]
                if image_filename not in downloaded_images:
                    print(f"移除: {event['year']}: {event['name']} -> {event['image']}")
                    del event['image']
                    removed_count += 1
                else:
                    kept_count += 1

# 保存更新后的JSON文件
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print()
print("=" * 60)
print("图片引用清理完成！")
print(f"保留有效图片: {kept_count} 个")
print(f"移除无效图片: {removed_count} 个")
print("=" * 60)
