import os

# 定义基础路径
base_path = r"e:\Test\读书笔记\创作-中华文明的底层算法与未来演化"
output_file = os.path.join(base_path, r"出版工作台\00_全书初稿_系统觉醒.md")

# 定义章节顺序
# 卷首语和章节文件
structure = [
    # 总纲
    (base_path, "00_总纲_文明的源代码.md"),
    
    # 第一卷
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "00_卷首语_秩序的物理学.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "01_良渚_神的算力与能量控制权.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "02_红山_玉的协议与去中心化共识.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "03_陶寺_时间的垄断与信息主权.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "04_二里头_青铜源代码与系统集成.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "05_殷墟_恐怖的数据库与云端献祭.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "06_西周_开源协议与礼乐区块链.md"),
    (os.path.join(base_path, "第一卷_熵减的代价_能量与信息的秩序博弈"), "07_春秋_铁的黑客与去中心化暴力.md"),
    
    # 第二卷
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "00_卷首语_反脆弱的算法.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "01_石峁_这一夜无论如何要活下去.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "02_秦_商鞅的算法监狱.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "03_汉_帝国的带宽管理.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "04_长城_农牧博弈的纳什均衡.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "05_魏晋_贵族的云端备份.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "06_北魏_系统的热更新.md"),
    (os.path.join(base_path, "第二卷_反脆弱的城墙_危机与系统的重组"), "07_隋唐_大运河与流量霸权.md"),
    
    # 第三卷
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "00_卷首语_文明的边缘计算.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "01_三星堆_神树下的异构计算.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "02_楚_非共识的浪漫.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "03_丝路_翻译局与协议握手.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "04_宋_纸币与虚拟化.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "05_明_防火墙与白银漏洞.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "06_晚清_系统的宕机与重启.md"),
    (os.path.join(base_path, "第三卷_接口与变异_异质文明的边缘计算"), "07_终章_奇点前夜的造山者.md"),
]

def merge_files():
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 写入书名和作者信息
        outfile.write("# 系统觉醒：中华文明的底层算法与未来演化\n\n")
        outfile.write("> 作者：[作者姓名]\n")
        outfile.write("> 日期：2026年3月1日\n\n")
        outfile.write("---\n\n")

        for folder, filename in structure:
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    # 添加分页符，方便转 PDF
                    outfile.write(f"\n\n<div style='page-break-after: always;'></div>\n\n")
                    outfile.write(content)
                    print(f"已合并: {filename}")
            except FileNotFoundError:
                print(f"警告: 文件未找到 {filepath}")
            except Exception as e:
                print(f"错误: {e}")

    print(f"\n全书合并完成！输出文件: {output_file}")

if __name__ == "__main__":
    merge_files()
