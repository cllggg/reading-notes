#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证JSON中引用的图片是否都存在
"""

import json
from pathlib import Path

JSON_FILE = Path(__file__).parent.parent / "dynasty_data_enhanced.json"
IMAGE_DIR = Path(__file__).parent

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取已下载的图片列表
downloaded_images = set([f.name for f in IMAGE_DIR.glob("*.jpg")])

# 检查JSON中引用的图片
missing_images = []
valid_images = []

for dynasty in data:
    if 'events' in dynasty:
        for event in dynasty['events']:
            if 'image' in event:
                image_filename = event['image'].split('/')[-1]
                if image_filename in downloaded_images:
                    valid_images.append((event['year'], event['name'], image_filename))
                else:
                    missing_images.append((event['year'], event['name'], image_filename))

print('JSON中引用的图片统计:')
print(f'有效图片: {len(valid_images)}')
print(f'缺失图片: {len(missing_images)}')
print()

if missing_images:
    print('缺失的图片:')
    for year, name, img in missing_images:
        print(f'  {year}: {name} -> {img}')
else:
    print('✓ 所有JSON中引用的图片都已下载！')
