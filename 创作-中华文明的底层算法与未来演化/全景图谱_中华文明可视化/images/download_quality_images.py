#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中华文明时间轴高质量真实图片下载脚本（百度/必应优化版）
"""

import os
import requests
import time
import json
from urllib.parse import quote, urlparse
from pathlib import Path
from PIL import Image
import io
import hashlib
import re

# 图片搜索和下载配置
IMAGE_DIR = Path(__file__).parent
IMAGE_DIR.mkdir(exist_ok=True)

# 最小图片尺寸和大小
MIN_WIDTH = 800
MIN_HEIGHT = 600
MIN_FILE_SIZE = 100 * 1024  # 100KB

# 已下载的图片URL哈希，避免重复
downloaded_urls = set()

# 图片事件列表（优化搜索关键词）
IMAGE_EVENTS = [
    # 史前文化
    {"filename": "yangshao_culture.jpg", "keywords": ["仰韶文化", "仰韶彩陶", "仰韶遗址", "新石器时代"], "description": "仰韶文化彩陶"},
    {"filename": "yangshao_pottery.jpg", "keywords": ["仰韶人面鱼纹盆", "半坡人面鱼纹盆", "仰韶彩陶"], "description": "仰韶人面鱼纹盆"},
    {"filename": "banpo_settlement.jpg", "keywords": ["半坡遗址", "半坡博物馆", "仰韶文化遗址"], "description": "半坡遗址"},
    {"filename": "yangshao_to_longshan.jpg", "keywords": ["龙山文化", "龙山黑陶", "蛋壳黑陶"], "description": "龙山文化黑陶"},
    
    {"filename": "hemudu_culture.jpg", "keywords": ["河姆渡文化", "河姆渡遗址", "河姆渡博物馆"], "description": "河姆渡文化"},
    {"filename": "hemudu_rice.jpg", "keywords": ["河姆渡稻作", "河姆渡水稻", "古代水稻"], "description": "河姆渡稻作农业"},
    {"filename": "hemudu_building.jpg", "keywords": ["河姆渡干栏式建筑", "河姆渡建筑", "古代木构建筑"], "description": "河姆渡干栏式建筑"},
    {"filename": "hemudu_to_liangzhu.jpg", "keywords": ["良渚文化", "良渚遗址", "良渚文明"], "description": "良渚文化"},
    
    {"filename": "liangzhu_culture.jpg", "keywords": ["良渚玉器", "良渚文化玉器", "新石器时代玉器"], "description": "良渚文化玉器"},
    {"filename": "liangzhu_water_system.jpg", "keywords": ["良渚水利", "良渚古城水利", "古代水利工程"], "description": "良渚水利系统"},
    {"filename": "mojiaoshan_palace.jpg", "keywords": ["莫角山遗址", "良渚莫角山", "良渚宫殿"], "description": "莫角山宫殿"},
    {"filename": "liangzhu_jade_cong.jpg", "keywords": ["良渚玉琮", "玉琮", "良渚文化玉琮"], "description": "良渚玉琮"},
    {"filename": "liangzhu_decline.jpg", "keywords": ["良渚文化衰落", "良渚文明消失", "良渚古城"], "description": "良渚文化衰落"},
    
    {"filename": "baodun_culture.jpg", "keywords": ["宝墩文化", "宝墩遗址", "古蜀文化"], "description": "宝墩文化"},
    {"filename": "sanxingdui_bronze.jpg", "keywords": ["三星堆青铜器", "三星堆青铜立人", "三星堆青铜面具"], "description": "三星堆青铜器"},
    {"filename": "sanxingdui_mask.jpg", "keywords": ["三星堆纵目面具", "三星堆青铜面具", "三星堆金面具"], "description": "三星堆纵目面具"},
    {"filename": "sanxingdui_pit.jpg", "keywords": ["三星堆祭祀坑", "三星堆考古", "三星堆遗址"], "description": "三星堆祭祀坑"},
    {"filename": "jinsha_gold_mask.jpg", "keywords": ["金沙金面具", "金沙遗址", "金沙太阳神鸟"], "description": "金沙金面具"},
    {"filename": "qin_conquer_shu.jpg", "keywords": ["秦灭巴蜀", "秦统一巴蜀", "古代战争图"], "description": "秦灭巴蜀"},
    
    # 夏商周
    {"filename": "dayu_water_control.jpg", "keywords": ["大禹治水", "大禹治水图", "古代治水"], "description": "大禹治水"},
    {"filename": "erlitou_palace.jpg", "keywords": ["二里头遗址", "二里头宫殿", "夏朝遗址"], "description": "二里头宫殿"},
    {"filename": "mingtiao_battle.jpg", "keywords": ["鸣条之战", "商汤灭夏", "古代战争"], "description": "鸣条之战"},
    
    {"filename": "shangtang_conquer_xia.jpg", "keywords": ["商汤", "商汤灭夏", "商朝建立"], "description": "商汤灭夏"},
    {"filename": "pangeng_move_yin.jpg", "keywords": ["盘庚迁殷", "商朝迁都", "殷墟"], "description": "盘庚迁殷"},
    {"filename": "wuding_prosperity.jpg", "keywords": ["武丁", "商朝武丁", "商朝青铜器"], "description": "武丁盛世"},
    {"filename": "muye_battle.jpg", "keywords": ["牧野之战", "周武王伐纣", "商周之战"], "description": "牧野之战"},
    
    # 秦汉
    {"filename": "qin_unification.jpg", "keywords": ["秦始皇", "秦始皇统一六国", "秦始皇画像"], "description": "秦始皇统一六国"},
    {"filename": "lingqu_canal.jpg", "keywords": ["灵渠", "灵渠遗址", "古代运河"], "description": "灵渠"},
    {"filename": "qinshihuang_death.jpg", "keywords": ["秦始皇陵", "兵马俑", "秦始皇陵兵马俑"], "description": "秦始皇陵兵马俑"},
    {"filename": "dazexiang_uprising.jpg", "keywords": ["陈胜吴广起义", "大泽乡起义", "秦末农民起义"], "description": "大泽乡起义"},
    
    {"filename": "guangwu_zhongxing.jpg", "keywords": ["光武中兴", "刘秀", "汉光武帝"], "description": "光武中兴"},
    {"filename": "cai_lun_paper.jpg", "keywords": ["蔡伦造纸", "造纸术", "古代造纸"], "description": "蔡伦造纸"},
    {"filename": "yellow_turban.jpg", "keywords": ["黄巾起义", "张角", "东汉末年"], "description": "黄巾起义"},
    {"filename": "red_cliff_battle.jpg", "keywords": ["赤壁之战", "三国赤壁", "火烧赤壁"], "description": "赤壁之战"},
    {"filename": "caopi_han.jpg", "keywords": ["曹丕", "魏文帝", "三国曹丕"], "description": "曹丕"},
    
    # 隋唐
    {"filename": "xuanwumen_incident.jpg", "keywords": ["玄武门之变", "李世民", "唐朝"], "description": "玄武门之变"},
    {"filename": "anxi_protectorate.jpg", "keywords": ["安西都护府", "唐朝西域", "丝绸之路"], "description": "安西都护府"},
    {"filename": "wu_zetian.jpg", "keywords": ["武则天", "女皇武则天", "武则天画像"], "description": "武则天"},
    {"filename": "anshi_rebellion.jpg", "keywords": ["安史之乱", "安禄山", "唐朝安史之乱"], "description": "安史之乱"},
    {"filename": "huangchao_uprising.jpg", "keywords": ["黄巢起义", "唐末农民起义", "黄巢"], "description": "黄巢起义"},
    
    # 宋元
    {"filename": "chenqiao_mutiny.jpg", "keywords": ["陈桥兵变", "赵匡胤", "宋朝建立"], "description": "陈桥兵变"},
    {"filename": "chanyuan_treaty.jpg", "keywords": ["澶渊之盟", "宋辽和约", "北宋澶渊"], "description": "澶渊之盟"},
    {"filename": "wang_ansi_reform.jpg", "keywords": ["王安石变法", "王安石", "北宋变法"], "description": "王安石变法"},
    {"filename": "jingkang_incident.jpg", "keywords": ["靖康之变", "靖康之耻", "北宋灭亡"], "description": "靖康之变"},
    {"filename": "yamen_battle.jpg", "keywords": ["崖山海战", "南宋灭亡", "崖山之战"], "description": "崖山海战"},
    
    # 明清
    {"filename": "zhu_yuanzhang.jpg", "keywords": ["朱元璋", "明太祖", "朱元璋画像"], "description": "朱元璋"},
    {"filename": "zheng_he_voyage.jpg", "keywords": ["郑和下西洋", "郑和宝船", "明朝航海"], "description": "郑和下西洋"},
    {"filename": "tumu_fortress.jpg", "keywords": ["土木堡之变", "明英宗", "土木之变"], "description": "土木堡之变"},
    {"filename": "yitiaobian_method.jpg", "keywords": ["一条鞭法", "张居正", "明朝改革"], "description": "一条鞭法"},
    {"filename": "jiashen_incident.jpg", "keywords": ["甲申之变", "明朝灭亡", "李自成"], "description": "甲申之变"},
    
    # 民国
    {"filename": "roc_establishment.jpg", "keywords": ["中华民国成立", "孙中山", "民国建立"], "description": "中华民国成立"},
    {"filename": "new_culture_movement.jpg", "keywords": ["新文化运动", "新青年", "五四新文化"], "description": "新文化运动"},
    {"filename": "may_fourth_movement.jpg", "keywords": ["五四运动", "五四爱国运动", "1919五四"], "description": "五四运动"},
    {"filename": "ccp_establishment.jpg", "keywords": ["中国共产党成立", "中共一大", "南湖红船"], "description": "中国共产党成立"},
    {"filename": "northern_expedition.jpg", "keywords": ["北伐战争", "国民革命军", "北伐"], "description": "北伐战争"},
    {"filename": "september_eighteenth_incident.jpg", "keywords": ["九一八事变", "九一八", "1931九一八"], "description": "九一八事变"},
    {"filename": "long_march.jpg", "keywords": ["长征", "红军长征", "二万五千里长征"], "description": "长征"},
    {"filename": "marco_polo_bridge.jpg", "keywords": ["七七事变", "卢沟桥事变", "七七卢沟桥"], "description": "七七事变"},
    {"filename": "anti_japanese_victory.jpg", "keywords": ["抗日战争胜利", "1945胜利", "日本投降"], "description": "抗日战争胜利"},
    {"filename": "prc_establishment.jpg", "keywords": ["中华人民共和国成立", "开国大典", "1949开国"], "description": "中华人民共和国成立"},
    
    # 新中国
    {"filename": "korean_war.jpg", "keywords": ["抗美援朝", "志愿军", "朝鲜战争"], "description": "抗美援朝"},
    {"filename": "taiwan_strait.jpg", "keywords": ["台湾海峡", "台海", "台湾"], "description": "台湾海峡"},
    {"filename": "first_five_year_plan.jpg", "keywords": ["第一个五年计划", "一五计划", "1953计划"], "description": "第一个五年计划"},
    {"filename": "first_constitution.jpg", "keywords": ["中华人民共和国宪法", "1954宪法", "中国宪法"], "description": "中华人民共和国宪法"},
    {"filename": "hundred_flowers.jpg", "keywords": ["百花齐放", "双百方针", "百花齐放百家争鸣"], "description": "百花齐放"},
    {"filename": "atomic_bomb.jpg", "keywords": ["第一颗原子弹", "中国原子弹", "1964原子弹"], "description": "第一颗原子弹"},
    {"filename": "dongfanghong_satellite.jpg", "keywords": ["东方红一号", "中国第一颗卫星", "1970卫星"], "description": "东方红一号"},
    {"filename": "un_seat.jpg", "keywords": ["恢复联合国合法席位", "中国联合国", "1971联合国"], "description": "恢复联合国合法席位"},
    {"filename": "reform_opening.jpg", "keywords": ["改革开放", "三中全会", "1978改革"], "description": "改革开放"},
    {"filename": "china_us_relations.jpg", "keywords": ["中美建交", "中美关系", "1979建交"], "description": "中美建交"},
    {"filename": "gaokao_restored.jpg", "keywords": ["恢复高考", "1977高考", "高考恢复"], "description": "恢复高考"},
    {"filename": "market_economy.jpg", "keywords": ["社会主义市场经济", "市场经济", "中国经济改革"], "description": "社会主义市场经济"},
    {"filename": "deng_southern_tour.jpg", "keywords": ["邓小平南巡", "南巡讲话", "1992南巡"], "description": "邓小平南巡"},
    {"filename": "1992_consensus.jpg", "keywords": ["九二共识", "两岸关系", "1992共识"], "description": "九二共识"},
    {"filename": "hongkong_handover.jpg", "keywords": ["香港回归", "1997香港", "香港交接"], "description": "香港回归"},
    {"filename": "macau_handover.jpg", "keywords": ["澳门回归", "1999澳门", "澳门交接"], "description": "澳门回归"},
    {"filename": "china_wto.jpg", "keywords": ["加入WTO", "中国入世", "2001WTO"], "description": "加入WTO"},
    {"filename": "shenzhou5.jpg", "keywords": ["神舟五号", "杨利伟", "2003神舟"], "description": "神舟五号"},
    {"filename": "change1.jpg", "keywords": ["嫦娥一号", "中国探月", "2007嫦娥"], "description": "嫦娥一号"},
    {"filename": "beijing_olympics.jpg", "keywords": ["北京奥运会", "2008奥运", "北京奥运开幕式"], "description": "北京奥运会"},
    {"filename": "second_largest_economy.jpg", "keywords": ["中国经济", "GDP", "世界第二大经济体"], "description": "中国经济"},
    {"filename": "chinese_dream.jpg", "keywords": ["中国梦", "民族复兴", "中国梦宣传"], "description": "中国梦"},
    {"filename": "belt_road.jpg", "keywords": ["一带一路", "丝绸之路", "一带一路倡议"], "description": "一带一路"},
    {"filename": "change4.jpg", "keywords": ["嫦娥四号", "月球背面", "2019嫦娥"], "description": "嫦娥四号"},
    {"filename": "beidou.jpg", "keywords": ["北斗卫星", "北斗导航", "北斗系统"], "description": "北斗卫星导航系统"},
    {"filename": "moderately_prosperous.jpg", "keywords": ["全面建成小康社会", "脱贫攻坚", "小康社会"], "description": "全面建成小康社会"},
    {"filename": "tianwen1.jpg", "keywords": ["天问一号", "火星探测", "2020天问"], "description": "天问一号"},
    {"filename": "space_station.jpg", "keywords": ["中国空间站", "天宫空间站", "空间站"], "description": "中国空间站"},
    {"filename": "beijing_winter_olympics.jpg", "keywords": ["北京冬奥会", "2022冬奥", "北京冬季奥运会"], "description": "北京冬奥会"},
    {"filename": "hangzhou_asian_games.jpg", "keywords": ["杭州亚运会", "2023亚运", "杭州亚运会开幕式"], "description": "杭州亚运会"},
]

def get_url_hash(url):
    """获取URL的哈希值"""
    return hashlib.md5(url.encode()).hexdigest()

def validate_image(image_data, filename):
    """验证图片是否有效"""
    try:
        img = Image.open(io.BytesIO(image_data))
        img.verify()
        
        # 重新打开图片（verify会关闭文件）
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
        
        # 检查尺寸
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return False, f"尺寸太小: {width}x{height}"
        
        # 检查文件大小
        if len(image_data) < MIN_FILE_SIZE:
            return False, f"文件太小: {len(image_data)} bytes"
        
        return True, (width, height)
        
    except Exception as e:
        return False, f"图片验证失败: {str(e)}"

def download_image(url, filename, max_retries=3):
    """下载并验证图片（带重试）"""
    for attempt in range(max_retries):
        try:
            # 检查是否重复下载
            url_hash = get_url_hash(url)
            if url_hash in downloaded_urls:
                return False
            downloaded_urls.add(url_hash)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Referer': 'https://www.baidu.com/'
            }
            
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # 读取图片数据
            image_data = response.content
            
            # 验证图片
            is_valid, result = validate_image(image_data, filename)
            
            if not is_valid:
                return False
            
            width, height = result
            
            # 保存图片
            filepath = IMAGE_DIR / filename
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"  ✓ 下载成功: {filename} (尺寸: {width}x{height}, 大小: {len(image_data)/1024:.1f}KB)")
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            continue
    
    return False

def search_baidu_images(keyword):
    """从百度图片搜索获取图片URL"""
    try:
        url = "https://image.baidu.com/search/acjson"
        params = {
            "tn": "resultjson_com",
            "logid": "",
            "ipn": "rj",
            "ct": "201326592",
            "is": "",
            "fp": "result",
            "fr": "",
            "word": keyword,
            "queryWord": keyword,
            "cl": "2",
            "lm": "-1",
            "ie": "utf-8",
            "oe": "utf-8",
            "adpicid": "",
            "st": "-1",
            "z": "",
            "ic": "0",
            "hd": "1",
            "latest": "",
            "copyright": "0",
            "s": "",
            "se": "",
            "tab": "",
            "width": "",
            "height": "",
            "face": "0",
            "istype": "2",
            "qc": "",
            "nc": "1",
            "expermode": "",
            "nojc": "0",
            "isAsync": "",
            "pn": "0",
            "rn": "30",
            "gsm": "1e",
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://image.baidu.com/'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if "data" in data:
            image_urls = []
            for item in data["data"]:
                if "middleURL" in item:
                    image_urls.append(item["middleURL"])
                elif "thumbURL" in item:
                    image_urls.append(item["thumbURL"])
            return image_urls
        
        return []
        
    except Exception as e:
        return []

def search_bing_images(keyword):
    """从必应图片搜索获取图片URL"""
    try:
        url = "https://www.bing.com/images/async"
        params = {
            "q": keyword,
            "first": "1",
            "count": "30",
            "tsc": "ImageBasicHover",
            "cw": "1920",
            "ch": "1080",
            "mkt": "zh-CN",
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.bing.com/images/search?q=' + quote(keyword)
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 从HTML中提取图片URL
        html = response.text
        pattern = r'"murl":"([^"]+)"'
        matches = re.findall(pattern, html)
        
        # 转义URL
        image_urls = []
        for match in matches:
            url = match.replace('\\u0026', '&').replace('\\u003d', '=').replace('\\u003f', '?')
            image_urls.append(url)
        
        return image_urls[:30]
        
    except Exception as e:
        return []

def download_from_search_engines(event):
    """从搜索引擎下载图片"""
    filename = event["filename"]
    keywords = event["keywords"]
    description = event["description"]
    
    print(f"正在下载: {filename} ({description})")
    
    # 尝试每个关键词
    for keyword in keywords:
        # 优先从百度搜索
        print(f"  尝试百度图片: {keyword}")
        image_urls = search_baidu_images(keyword)
        
        for url in image_urls:
            if download_image(url, filename):
                return True
            time.sleep(0.3)
        
        # 如果百度失败，尝试必应
        print(f"  尝试必应图片: {keyword}")
        image_urls = search_bing_images(keyword)
        
        for url in image_urls:
            if download_image(url, filename):
                return True
            time.sleep(0.3)
    
    print(f"  ✗ 所有来源都失败")
    return False

def main():
    """主函数"""
    print("=" * 60)
    print("中华文明时间轴高质量真实图片下载工具（百度/必应优化版）")
    print("=" * 60)
    print(f"图片保存目录: {IMAGE_DIR}")
    print(f"最小尺寸: {MIN_WIDTH}x{MIN_HEIGHT}")
    print(f"最小文件大小: {MIN_FILE_SIZE/1024:.1f}KB")
    print()
    
    success_count = 0
    fail_count = 0
    
    for event in IMAGE_EVENTS:
        filename = event["filename"]
        
        if (IMAGE_DIR / filename).exists():
            print(f"⊘ 跳过已存在: {filename}")
            success_count += 1
            continue
        
        if download_from_search_engines(event):
            success_count += 1
        else:
            fail_count += 1
        
        time.sleep(1)
    
    print()
    print("=" * 60)
    print(f"下载完成！")
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    print(f"成功率: {success_count/(success_count+fail_count)*100:.1f}%")
    print("=" * 60)
    print()
    print("提示：")
    print("- 所有下载的图片都已验证，确保可以正常打开")
    print("- 图片尺寸 >= 800x600，文件大小 >= 100KB")
    print("- 优先从百度图片和必应图片下载")
    print("- 如果有下载失败的图片，可以手动从其他来源下载")

if __name__ == "__main__":
    main()
