import os
import re
import json
import sys

def zh_to_arabic(zh_num):
    """
    中文数字转换为阿拉伯数字
    """
    zh_map = {
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
        '十一': '11', '十二': '12', '十三': '13', '十四': '14', '十五': '15',
        '十六': '16', '十七': '17', '十八': '18', '十九': '19', '二十': '20',
        '二十一': '21', '二十二': '22', '二十三': '23', '二十四': '24', '二十五': '25',
        '二十六': '26', '二十七': '27', '二十八': '28', '二十九': '29', '三十': '30',
        '三十一': '31', '三十二': '32', '三十三': '33', '三十四': '34', '三十五': '35',
        '三十六': '36', '三十七': '37', '三十八': '38', '三十九': '39', '四十': '40',
        '四十一': '41', '四十二': '42', '四十三': '43', '四十四': '44', '四十五': '45',
        '四十六': '46', '四十七': '47', '四十八': '48', '四十九': '49', '五十': '50',
        '五十一': '51', '五十二': '52', '五十三': '53', '五十四': '54', '五十五': '55',
        '五十六': '56', '五十七': '57', '五十八': '58', '五十九': '59', '六十': '60',
        '六十一': '61', '六十二': '62', '六十三': '63', '六十四': '64'
    }
    return zh_map.get(zh_num, zh_num)

def parse_markdown(content):
    """
    解析易经Markdown文本，返回结构化数据字典。
    输入：Markdown文本字符串
    输出：按卦序号索引的字典
    """
    guas = {}
    
    # 使用正则表达式分割每个卦
    # 每个卦以 "## 第n卦" 开头，直到下一个 "## 第n+1卦" 或文件结束
    # 匹配中文数字，如：第一卦、第二卦...
    gua_pattern = r'##\s*第(\S+?)\s*卦\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)'
    
    # 找到所有卦的起始位置
    positions = []
    for match in re.finditer(gua_pattern, content, re.MULTILINE):
        positions.append((match.start(), match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)))
    
    # 如果没有找到匹配，尝试其他格式
    if not positions:
        # 尝试匹配 "## 第一卦 乾 乾为天 乾上乾下"
        gua_pattern2 = r'##\s*(\S+?)\s*卦\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)\s*([^\s]+)'
        for match in re.finditer(gua_pattern2, content, re.MULTILINE):
            positions.append((match.start(), match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)))
    
    # 为每个卦提取内容
    for i in range(len(positions)):
        start_pos = positions[i][0]
        if i + 1 < len(positions):
            end_pos = positions[i + 1][0]
        else:
            end_pos = len(content)
        
        gua_content = content[start_pos:end_pos]
        
        # 提取卦信息
        gua_num = zh_to_arabic(positions[i][1])  # 转换中文数字为阿拉伯数字
        gua_name = positions[i][2]
        gua_full_name = positions[i][3]
        gua_symbol = positions[i][4] + positions[i][5]
        
        # 初始化卦数据结构
        gua_data = {
            'name': gua_name,
            'symbol': gua_symbol,
            'full_name': gua_full_name,
            'gua_ci': '',
            'tuan': '',
            'xiang': '',
            'yao': {}
        }
        
        # 提取卦辞（卦名后的第一段）
        # 格式如：乾：元，亨，利，贞。
        gua_ci_match = re.search(r'{}：\s*([^\n]+)'.format(gua_name), gua_content)
        if gua_ci_match:
            gua_data['gua_ci'] = gua_ci_match.group(1).strip()
        
        # 提取彖曰
        tuan_match = re.search(r'彖曰[：:]\s*(.+?)(?=\n\s*\n|\n\s*象曰|$)', gua_content, re.DOTALL)
        if tuan_match:
            gua_data['tuan'] = tuan_match.group(1).strip()
        
        # 提取象曰（大象辞）
        xiang_match = re.search(r'象曰[：:]\s*(.+?)(?=\n\s*\n|\n\s*初六|$)', gua_content, re.DOTALL)
        if xiang_match:
            gua_data['xiang'] = xiang_match.group(1).strip()
        
        # 提取爻辞
        # 爻辞格式：初九：潜龙，勿用。 或 初九：潜龙，勿用。
        yao_pattern = r'([初上二三四五六][九六]?)[：:]\s*([^\n。]+[。])'
        yao_matches = re.findall(yao_pattern, gua_content)
        
        for yao_name, yao_text in yao_matches:
            gua_data['yao'][yao_name] = {
                'text': yao_text.strip(),
                'xiang': ''
            }
        
        # 提取爻象辞（简化处理）
        yao_xiang_pattern = r'{}[：:]\s*([^\n。]+[。])'.format(gua_name)
        yao_xiang_matches = re.findall(yao_xiang_pattern, gua_content)
        # 注意：实际情况更复杂，此处为示例
        
        # 将卦数据存入字典
        guas[gua_num] = gua_data
    
    return guas

def main():
    if len(sys.argv) != 3:
        print("用法: python parse_markdown.py <输入文件> <输出文件>")
        print("示例: python parse_markdown.py data/yijing_full.md instance/data/yijing_data.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        sys.exit(1)
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析内容
    guas = parse_markdown(content)
    
    # 保存为JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(guas, f, ensure_ascii=False, indent=2, sort_keys=True)
    
    print(f"成功解析 {len(guas)} 卦，并保存为 {output_file}")

if __name__ == '__main__':
    main()