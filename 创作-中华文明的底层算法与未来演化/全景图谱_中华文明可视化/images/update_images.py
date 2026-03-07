#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将已下载的图片关联到JSON文件中对应的事件
"""

import json
from pathlib import Path

JSON_FILE = Path(__file__).parent.parent / "dynasty_data_enhanced.json"
IMAGE_DIR = Path(__file__).parent

# 事件名称到图片文件的映射（根据JSON文件中的实际名称）
EVENT_IMAGE_MAP = {
    # 史前文化
    "仰韶文化兴起": "images/yangshao_culture.jpg",
    "彩陶制作高峰期": "images/yangshao_pottery.jpg",
    "半坡类型繁荣": "images/banpo_settlement.jpg",
    "仰韶文化转型为龙山文化": "images/yangshao_to_longshan.jpg",
    
    "河姆渡文化兴起": "images/hemudu_culture.jpg",
    "稻作农业成熟": "images/hemudu_rice.jpg",
    "干栏式建筑普及": "images/hemudu_building.jpg",
    "河姆渡文化被良渚文化继承": "images/hemudu_to_liangzhu.jpg",
    
    "良渚文化兴起": "images/liangzhu_culture.jpg",
    "开始修建大型水利系统": "images/liangzhu_water_system.jpg",
    "莫角山宫殿区建成": "images/mojiaoshan_palace.jpg",
    "反山大墓建成，玉琮王出土": "images/liangzhu_jade_cong.jpg",
    "良渚文化衰亡": "images/liangzhu_decline.jpg",
    
    "宝墩文化兴起": "images/baodun_culture.jpg",
    "三星堆文化鼎盛": "images/sanxingdui_bronze.jpg",
    "青铜神树、纵目面具制作": "images/sanxingdui_mask.jpg",
    "最后一场大祭，祭祀坑掩埋": "images/sanxingdui_pit.jpg",
    "金沙时期，政治中心转移": "images/jinsha_gold_mask.jpg",
    "秦灭巴蜀，古蜀亡": "images/qin_conquer_shu.jpg",
    
    # 夏商周
    "大禹治水成功，建立夏朝": "images/dayu_water_control.jpg",
    "二里头文化兴起": "images/erlitou_palace.jpg",
    "鸣条之战，夏亡": "images/mingtiao_battle.jpg",
    
    "商汤灭夏": "images/shangtang_conquer_xia.jpg",
    "盘庚迁殷": "images/pangeng_move_yin.jpg",
    "武丁盛世": "images/wuding_prosperity.jpg",
    "牧野之战，商亡": "images/muye_battle.jpg",
    
    # 秦汉
    "秦始皇统一六国": "images/qin_unification.jpg",
    "征服百越，修筑灵渠": "images/lingqu_canal.jpg",
    "秦始皇驾崩": "images/qinshihuang_death.jpg",
    "陈胜吴广起义": "images/dazexiang_uprising.jpg",
    
    "光武中兴": "images/guangwu_zhongxing.jpg",
    "蔡伦改进造纸术": "images/cai_lun_paper.jpg",
    "黄巾起义": "images/yellow_turban.jpg",
    "赤壁之战": "images/red_cliff_battle.jpg",
    "曹丕代汉": "images/caopi_han.jpg",
    
    # 隋唐
    "玄武门之变": "images/xuanwumen_incident.jpg",
    "设立安西都护府": "images/anxi_protectorate.jpg",
    "武则天称帝": "images/wu_zetian.jpg",
    "安史之乱": "images/anshi_rebellion.jpg",
    "黄巢起义": "images/huangchao_uprising.jpg",
    
    # 宋元
    "陈桥兵变": "images/chenqiao_mutiny.jpg",
    "澶渊之盟": "images/chanyuan_treaty.jpg",
    "王安石变法": "images/wang_ansi_reform.jpg",
    "靖康之变": "images/jingkang_incident.jpg",
    "崖山海战": "images/yamen_battle.jpg",
    
    # 明清
    "朱元璋建立明朝": "images/zhu_yuanzhang.jpg",
    "郑和下西洋": "images/zheng_he_voyage.jpg",
    "土木堡之变": "images/tumu_fortress.jpg",
    "一条鞭法": "images/yitiaobian_method.jpg",
    "甲申之变": "images/jiashen_incident.jpg",
    
    # 民国
    "中华民国成立": "images/roc_establishment.jpg",
    "新文化运动": "images/new_culture_movement.jpg",
    "五四运动": "images/may_fourth_movement.jpg",
    "中国共产党成立": "images/ccp_establishment.jpg",
    "北伐战争": "images/northern_expedition.jpg",
    "九一八事变": "images/september_eighteenth_incident.jpg",
    "长征": "images/long_march.jpg",
    "七七事变": "images/marco_polo_bridge.jpg",
    "抗日战争胜利": "images/anti_japanese_victory.jpg",
    "中华人民共和国成立": "images/prc_establishment.jpg",
    
    # 新中国
    "抗美援朝战争": "images/korean_war.jpg",
    "台湾海峡危机": "images/taiwan_strait.jpg",
    "第一个五年计划": "images/first_five_year_plan.jpg",
    "第一部宪法颁布": "images/first_constitution.jpg",
    "百花齐放百家争鸣": "images/hundred_flowers.jpg",
    "第一颗原子弹爆炸": "images/atomic_bomb.jpg",
    "东方红一号卫星": "images/dongfanghong_satellite.jpg",
    "恢复联合国合法席位": "images/un_seat.jpg",
    "改革开放": "images/reform_opening.jpg",
    "中美建交": "images/china_us_relations.jpg",
    "恢复高考": "images/gaokao_restored.jpg",
    "社会主义市场经济": "images/market_economy.jpg",
    "邓小平南巡讲话": "images/deng_southern_tour.jpg",
    "九二共识": "images/1992_consensus.jpg",
    "香港回归": "images/hongkong_handover.jpg",
    "澳门回归": "images/macau_handover.jpg",
    "加入WTO": "images/china_wto.jpg",
    "神舟五号载人航天": "images/shenzhou5.jpg",
    "嫦娥一号卫星": "images/change1.jpg",
    "北京奥运会": "images/beijing_olympics.jpg",
    "中国经济": "images/second_largest_economy.jpg",
    "中国梦": "images/chinese_dream.jpg",
    "一带一路": "images/belt_road.jpg",
    "嫦娥四号": "images/change4.jpg",
    "北斗三号全球组网": "images/beidou.jpg",
    "全面建成小康社会": "images/moderately_prosperous.jpg",
    "天问一号火星探测": "images/tianwen1.jpg",
    "中国空间站": "images/space_station.jpg",
    "北京冬奥会": "images/beijing_winter_olympics.jpg",
    "杭州亚运会": "images/hangzhou_asian_games.jpg",
}

# 读取JSON文件
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取已下载的图片列表
downloaded_images = set([f.name for f in IMAGE_DIR.glob("*.jpg")])

# 统计更新情况
updated_count = 0
already_has_image_count = 0
no_image_available_count = 0

# 更新事件图片
for dynasty in data:
    if "events" in dynasty:
        for event in dynasty["events"]:
            event_name = event["name"]
            
            # 如果事件已经有图片字段，检查图片是否存在
            if "image" in event:
                image_filename = event["image"].split("/")[-1]
                if image_filename in downloaded_images:
                    already_has_image_count += 1
                else:
                    # 图片不存在，尝试从映射中查找
                    if event_name in EVENT_IMAGE_MAP:
                        new_image = EVENT_IMAGE_MAP[event_name]
                        new_image_filename = new_image.split("/")[-1]
                        if new_image_filename in downloaded_images:
                            event["image"] = new_image
                            updated_count += 1
                            print(f"更新: {event_name} -> {new_image}")
            else:
                # 事件没有图片字段，尝试从映射中查找
                if event_name in EVENT_IMAGE_MAP:
                    new_image = EVENT_IMAGE_MAP[event_name]
                    new_image_filename = new_image.split("/")[-1]
                    if new_image_filename in downloaded_images:
                        event["image"] = new_image
                        updated_count += 1
                        print(f"添加: {event_name} -> {new_image}")
                    else:
                        no_image_available_count += 1
                else:
                    no_image_available_count += 1

# 保存更新后的JSON文件
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print()
print("=" * 60)
print("图片关联完成！")
print(f"已添加图片: {updated_count} 个")
print(f"已有有效图片: {already_has_image_count} 个")
print(f"无可用图片: {no_image_available_count} 个")
print("=" * 60)
