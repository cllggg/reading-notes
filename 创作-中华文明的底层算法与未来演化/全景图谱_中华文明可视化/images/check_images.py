#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查JSON文件中哪些事件缺少图片
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

# 统计缺少图片的事件
events_without_image = []
events_with_image = []

for dynasty in data:
    if "events" in dynasty:
        for event in dynasty["events"]:
            if "image" in event:
                image_filename = event["image"].split("/")[-1]
                if image_filename in downloaded_images:
                    events_with_image.append({
                        "year": event["year"],
                        "name": event["name"],
                        "image": event["image"]
                    })
                else:
                    events_without_image.append({
                        "year": event["year"],
                        "name": event["name"],
                        "image": event["image"]
                    })
            else:
                events_without_image.append({
                    "year": event["year"],
                    "name": event["name"],
                    "image": None
                })

print("=" * 60)
print("图片关联情况统计")
print("=" * 60)
print(f"已下载图片总数: {len(downloaded_images)}")
print(f"有图片的事件: {len(events_with_image)}")
print(f"缺少图片的事件: {len(events_without_image)}")
print()

if events_with_image:
    print("已关联图片的事件（前20个）:")
    for i, event in enumerate(sorted(events_with_image, key=lambda x: x["year"])[:20]):
        print(f"  {event['year']}: {event['name']} -> {event['image']}")
    print()

if events_without_image:
    print("缺少图片的事件:")
    for event in sorted(events_without_image, key=lambda x: x["year"]):
        if event["image"]:
            print(f"  {event['year']}: {event['name']} -> {event['image']} (图片未下载)")
        else:
            print(f"  {event['year']}: {event['name']} -> 无图片字段")
