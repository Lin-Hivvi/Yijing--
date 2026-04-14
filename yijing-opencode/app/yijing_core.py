import json
import random

class YiJing:
    """
    《易经》核心查询类。
    负责从 JSON 数据中加载六十四卦，并提供起卦算法与检索功能。
    """
    
    def __init__(self, data_path='instance/data/yijing_data.json'):
        """
        加载结构化数据
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            self.gua_data = json.load(f)
        self.gua_count = len(self.gua_data)
        print(f"已加载 {self.gua_count} 卦数据")
    
    def generate_divination(self):
        """
        模拟大衍筮法起卦过程。
        采用 6 次随机数 (6,7,8,9) 模拟营数。
        返回: 本卦索引, 变卦索引, 动爻列表
        6: 老阴 (⚋) 变阳爻
        7: 少阳 (⚊) 不变
        8: 少阴 (⚋) 不变  
        9: 老阳 (⚊) 变阴爻
        """
        # 生成六爻
        yao_results = []
        changing_lines = []  # 动爻列表 (0-5对应初爻到上爻)
        
        for i in range(6):
            # 模拟大衍筮法概率分布：6/16, 7/16, 8/16, 9/16
            num = random.choices([6, 7, 8, 9], weights=[1, 3, 5, 7])[0]
            yao_results.append(num)
            
            # 记录动爻（老阴或老阳）
            if num == 6:  # 老阴，变阳
                changing_lines.append(i)
            elif num == 9:  # 老阳，变阴
                changing_lines.append(i)
        
        # 根据爻数计算本卦和变卦索引
        base_gua = self._calculate_gua_index(yao_results, changing_yi=False)
        changing_gua = self._calculate_gua_index(yao_results, changing_yi=True) if changing_lines else base_gua
        
        return str(base_gua), str(changing_gua), changing_lines
    
    def _calculate_gua_index(self, yao_results, changing_yi=False):
        """
        根据爻数计算卦的索引 (1-64)。
        yao_results: 六爻列表，每个元素是6,7,8,9
        changing_yi: 是否考虑变爻（计算变卦）
        二进制表示：阳爻为1，阴爻为0
        """
        binary_str = ''
        for num in yao_results:
            if changing_yi:
                # 计算变卦时，老阴变阳，老阳变阴
                if num == 6:  # 老阴变阳
                    binary_str = '1' + binary_str
                elif num == 9:  # 老阳变阴
                    binary_str = '0' + binary_str
                else:  # 少阳(7)少阴(8)不变
                    binary_str = ('1' if num == 7 else '0') + binary_str
            else:
                # 本卦：直接判断阴阳
                binary_str = ('1' if num in [7, 9] else '0') + binary_str
        
        # 二进制转换为十进制
        index = int(binary_str, 2) + 1
        
        # 确保索引在有效范围内 (1 - gua_count)
        if index < 1 or index > self.gua_count:
            index = (index % self.gua_count) or 1
        
        return index
    
    def get_gua_details(self, gua_id, changing_lines=None):
        """
        根据卦ID获取渲染所需的所有文本。
        特别处理：如果有动爻，需高亮显示对应的爻辞。
        
        参数:
            gua_id: 卦的索引 (字符串或整数)
            changing_lines: 动爻列表，每个元素是爻的位置 (0-5)
        
        返回:
            包含卦信息的字典
        """
        # 确保卦ID在有效范围内
        gua_key = str(gua_id)
        if gua_key not in self.gua_data:
            # 如果卦ID不存在，使用第一个卦作为默认
            gua_key = '1'
            print(f"警告：卦ID {gua_id} 不存在，使用默认卦 {gua_key}")
        
        gua = self.gua_data[gua_key].copy()
        
        # 获取爻顺序列表（从初爻到上爻）
        yao_order = ['初九', '六二', '九三', '六四', '九五', '上六']
        
        # 重新排序爻辞，确保顺序正确
        sorted_yao = {}
        for i, yao_name in enumerate(yao_order):
            # 根据阴阳调整爻名
            if str(gua_id) == '1':  # 乾卦特殊处理
                yao_name = ['初九', '九二', '九三', '九四', '九五', '上九'][i]
            elif str(gua_id) == '2':  # 坤卦特殊处理
                yao_name = ['初六', '六二', '六三', '六四', '六五', '上六'][i]
            
            # 尝试查找爻辞
            if yao_name in gua['yao']:
                sorted_yao[yao_name] = gua['yao'][yao_name]
            else:
                # 如果精确匹配失败，尝试模糊匹配
                for key in gua['yao']:
                    if key.endswith(yao_name[-1]) or key.startswith(yao_name[0]):
                        sorted_yao[yao_name] = gua['yao'][key]
                        break
        
        gua['sorted_yao'] = sorted_yao
        
        # 标记动爻
        if changing_lines:
            gua['changing_lines'] = changing_lines
            gua['changing_yao_texts'] = []
            for line_pos in changing_lines:
                # 计算爻名
                if line_pos == 0:
                    yao_name = '初九' if str(gua_id) == '1' else '初六'
                elif line_pos == 1:
                    yao_name = '九二' if str(gua_id) == '1' else '六二'
                elif line_pos == 2:
                    yao_name = '九三' if str(gua_id) == '1' else '六三'
                elif line_pos == 3:
                    yao_name = '九四' if str(gua_id) == '1' else '六四'
                elif line_pos == 4:
                    yao_name = '九五' if str(gua_id) == '1' else '六五'
                else:
                    yao_name = '上九' if str(gua_id) == '1' else '上六'
                
                if yao_name in gua['sorted_yao']:
                    gua['changing_yao_texts'].append({
                        'name': yao_name,
                        'text': gua['sorted_yao'][yao_name]['text']
                    })
        
        return gua
    
    def get_all_guas(self):
        """
        获取所有卦的基本信息列表。
        用于下拉菜单或检索页面。
        """
        gua_list = []
        for gua_id in sorted(self.gua_data.keys(), key=int):
            gua = self.gua_data[gua_id]
            gua_list.append({
                'id': gua_id,
                'name': gua['name'],
                'full_name': gua['full_name'],
                'gua_ci': gua['gua_ci'][:50] + '...' if len(gua['gua_ci']) > 50 else gua['gua_ci']
            })
        return gua_list
    
    def draw_yao_symbol(self, num):
        """
        根据数字返回爻符号
        6: 老阴 ⚋
        7: 少阳 ⚊  
        8: 少阴 ⚋
        9: 老阳 ⚊
        """
        if num == 6:
            return '⚋', '老阴 (变阳)'
        elif num == 7:
            return '⚊', '少阳'
        elif num == 8:
            return '⚋', '少阴'
        elif num == 9:
            return '⚊', '老阳 (变阴)'
        else:
            return '?', '未知'