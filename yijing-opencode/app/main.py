from flask import Flask, render_template, request, jsonify, redirect, url_for
from yijing_core import YiJing
import os
import json

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# 初始化易经核心类
# 使用相对于app目录的路径
data_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'data', 'yijing_data.json')
yijing = YiJing(data_path)

# 观测者效应文案
OBSERVER_EFFECT_TEXT = """
<h4>量子易理提示</h4>
<p>根据现代物理学中的「观测者效应」，系统在为您生成卦象的瞬间，已干预了原本叠加态的「可能性云」。此卦象是您当前心念与算法随机性共同作用下的「坍缩结果」。</p>
<p><strong>《易》为君子谋，不为小人谋。</strong> 请将此视为一面镜子，观照内心，而非机械地预测未来。善易者不卜。</p>
"""

@app.route('/')
def index():
    """
    首页：展示太极图或简洁界面，按钮「诚心起卦」
    """
    return render_template('index.html', page_title='易镜 · 起卦')

@app.route('/divinate', methods=['POST'])
def divinate():
    """
    处理起卦请求，返回卦象结果
    """
    # 生成卦象
    base_gua_id, changing_gua_id, changing_lines = yijing.generate_divination()
    
    # 获取卦象详情
    base_gua = yijing.get_gua_details(base_gua_id, changing_lines)
    changing_gua = yijing.get_gua_details(changing_gua_id)
    
    if not base_gua or not changing_gua:
        return jsonify({'error': '卦象数据获取失败'}), 500
    
    # 生成爻象符号显示
    yao_symbols = ['⚊', '⚋', '⚊', '⚋', '⚊', '⚋']  # 默认符号
    
    # 准备响应数据
    result = {
        'success': True,
        'base_gua': {
            'id': base_gua_id,
            'name': base_gua['name'],
            'full_name': base_gua['full_name'],
            'symbol': base_gua['symbol'],
            'gua_ci': base_gua['gua_ci'],
            'tuan': base_gua['tuan'],
            'xiang': base_gua['xiang']
        },
        'changing_gua': {
            'id': changing_gua_id,
            'name': changing_gua['name'],
            'full_name': changing_gua['full_name'],
            'symbol': changing_gua['symbol']
        },
        'changing_lines': changing_lines,
        'changing_yao_texts': base_gua.get('changing_yao_texts', []),
        'observer_effect': OBSERVER_EFFECT_TEXT,
        'is_changing': len(changing_lines) > 0,
        'yao_symbols': yao_symbols
    }
    
    # 如果请求是AJAX，返回JSON，否则渲染结果页
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(result)
    else:
        return render_template('result.html', **result)

@app.route('/search', methods=['GET'])
def search():
    """
    卦象检索页面
    """
    gua_id = request.args.get('id')
    gua_name = request.args.get('name', '')
    
    # 如果提供了卦ID，直接显示该卦
    if gua_id:
        try:
            gua = yijing.get_gua_details(gua_id)
            if gua:
                return render_template('search.html', 
                                     page_title=f"卦象检索 - {gua['name']}",
                                     gua=gua,
                                     gua_list=yijing.get_all_guas(),
                                     observer_effect=OBSERVER_EFFECT_TEXT)
        except:
            pass
    
    # 如果没有指定卦，显示列表
    return render_template('search.html', 
                         page_title='卦象检索',
                         gua=None,
                         gua_list=yijing.get_all_guas(),
                         observer_effect=OBSERVER_EFFECT_TEXT)

@app.route('/api/guas')
def api_guas():
    """
    API接口：获取所有卦列表
    """
    return jsonify(yijing.get_all_guas())

@app.route('/api/gua/<gua_id>')
def api_gua(gua_id):
    """
    API接口：获取指定卦详情
    """
    gua = yijing.get_gua_details(gua_id)
    if gua:
        return jsonify(gua)
    else:
        return jsonify({'error': '卦象不存在'}), 404

@app.route('/interpret', methods=['GET', 'POST'])
def interpret():
    """
    详细解卦页面
    提供卦象的深入分析和各个方面的解读
    """
    if request.method == 'POST':
        # 从表单获取数据
        base_gua_id = request.form.get('base_gua_id', '')
        changing_gua_id = request.form.get('changing_gua_id', '')
        changing_lines_str = request.form.get('changing_lines', '')
        question = request.form.get('question', '')
        focus_area = request.form.get('focus_area', 'general')  # 关注领域
        
        # 解析动爻列表
        changing_lines = []
        if changing_lines_str:
            try:
                # 解析JSON格式的动爻列表
                changing_lines = json.loads(changing_lines_str)
            except:
                # 尝试解析其他格式
                changing_lines = [int(x.strip()) for x in changing_lines_str.split(',') if x.strip().isdigit()]
    else:
        # GET请求，从查询参数获取
        base_gua_id = request.args.get('base_gua_id', '')
        changing_gua_id = request.args.get('changing_gua_id', '')
        changing_lines_str = request.args.get('changing_lines', '')
        question = request.args.get('question', '')
        focus_area = request.args.get('focus_area', 'general')
        
        # 解析动爻列表
        changing_lines = []
        if changing_lines_str:
            try:
                changing_lines = [int(x) for x in changing_lines_str.split(',')]
            except:
                changing_lines = []
    
    # 如果没有基础卦ID，重定向到首页
    if not base_gua_id:
        return redirect(url_for('index'))
    
    # 获取卦象详情
    base_gua = yijing.get_gua_details(base_gua_id, changing_lines)
    changing_gua = None
    if changing_gua_id and changing_gua_id != base_gua_id:
        changing_gua = yijing.get_gua_details(changing_gua_id)
    
    if not base_gua:
        return render_template('error.html',
                             page_title='解卦失败',
                             error_message='无法获取卦象信息，请重新起卦'), 400
    
    # 生成详细的解卦分析
    interpretation = generate_interpretation(base_gua, changing_gua, changing_lines, question, focus_area)
    
    return render_template('interpretation.html',
                         page_title=f"详细解卦 - {base_gua['name']}卦",
                         base_gua=base_gua,
                         changing_gua=changing_gua,
                         changing_lines=changing_lines,
                         question=question,
                         focus_area=focus_area,
                         interpretation=interpretation,
                         observer_effect=OBSERVER_EFFECT_TEXT)

def generate_interpretation(base_gua, changing_gua, changing_lines, question, focus_area):
    """
    生成详细的解卦分析
    基于网络搜索到的易经解卦知识和常见解读方法
    """
    interpretation = {
        'basic_meaning': '',
        'changing_meaning': '',
        'line_interpretations': [],
        'area_specific': {},
        'advice': '',
        'warning': '',
        'cultural_notes': []
    }
    
    # 基础卦义
    interpretation['basic_meaning'] = f"《{base_gua['full_name']}》{base_gua['gua_ci']}"
    
    # 彖辞解释
    if base_gua.get('tuan'):
        interpretation['basic_meaning'] += f"\n\n彖曰：{base_gua['tuan']}"
    
    # 象辞解释
    if base_gua.get('xiang'):
        interpretation['basic_meaning'] += f"\n\n象曰：{base_gua['xiang']}"
    
    # 动爻解释
    if changing_lines:
        interpretation['changing_meaning'] = "本次占卜有动爻，表示事物正在变化发展中：\n"
        for i, line_pos in enumerate(changing_lines):
            line_name = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'][line_pos]
            interpretation['changing_meaning'] += f"{line_name}变动，代表相应层面的变化。\n"
    
    # 变卦解释
    if changing_gua:
        interpretation['changing_meaning'] += f"\n变卦为《{changing_gua['full_name']}》，意味着事情发展的最终趋向。"
    
    # 爻辞解释
    if base_gua.get('sorted_yao'):
        interpretation['line_interpretations'] = []
        for yao_name, yao_info in base_gua['sorted_yao'].items():
            line_meaning = f"{yao_name}：{yao_info['text']}"
            interpretation['line_interpretations'].append(line_meaning)
    
    # 根据关注领域提供针对性解读
    focus_areas = {
        'career': '事业工作',
        'relationship': '感情婚姻', 
        'health': '健康养生',
        'wealth': '财运投资',
        'study': '学业考试',
        'general': '综合运势'
    }
    
    area_name = focus_areas.get(focus_area, '综合运势')
    
    # 基于卦名的通用解读（这里可以根据网络搜索到的内容扩展）
    gua_name = base_gua['name']
    gua_meanings = {
        '乾': '乾卦象征天，代表刚健、创造、领导。主事业顺利，但需注意不可太过刚强。',
        '坤': '坤卦象征地，代表柔顺、包容、承载。主人际关系和谐，但需注意不可过于被动。',
        '屯': '屯卦象征初生，代表艰难、积聚、开始。主创业艰难，但坚持终有收获。',
        '蒙': '蒙卦象征启蒙，代表教育、学习、开发。主学业进步，但需虚心求教。',
        '需': '需卦象征等待，代表需求、期待、时机。主需要耐心等待时机，不可急躁。',
        '未济': '未济卦象征未完成，代表过渡、变化、希望。主事情尚未完成，但充满希望。'
    }
    
    base_advice = gua_meanings.get(gua_name, '此卦象提示需审时度势，灵活应对。')
    
    # 根据不同领域提供建议
    area_advice = {
        'career': {
            '乾': '事业发展顺利，适合开拓新领域，展现领导才能。',
            '坤': '工作中需注重团队合作，以柔克刚，稳扎稳打。',
            '屯': '创业初期困难重重，需打好基础，积累资源。',
            '蒙': '需要学习新技能，接受培训，提升专业能力。',
            '需': '耐心等待晋升机会，不宜贸然行动。',
            '未济': '项目尚未完成，需坚持到底，不可半途而废。'
        },
        'relationship': {
            '乾': '感情中需展现担当，但不可过于强势。',
            '坤': '关系和睦，相互包容，注重家庭和谐。',
            '屯': '感情处于萌芽阶段，需要时间和耐心培养。',
            '蒙': '需要互相学习理解，增进沟通。',
            '需': '等待合适的缘分，不可强求。',
            '未济': '关系尚在发展中，需要进一步磨合。'
        },
        'health': {
            '乾': '注意头部和神经系统健康，避免过度劳累。',
            '坤': '注重脾胃保养，保持情绪稳定。',
            '屯': '初病需及时治疗，注意休息调养。',
            '蒙': '通过学习健康知识改善生活习惯。',
            '需': '需要适当休息，等待身体恢复。',
            '未济': '慢性病需长期调理，保持耐心。'
        }
    }
    
    area_specific = area_advice.get(focus_area, {}).get(gua_name, base_advice)
    interpretation['area_specific'][area_name] = area_specific
    
    # 总体建议
    interpretation['advice'] = f"对于「{area_name}」方面的建议：{area_specific}"
    
    # 注意事项
    if changing_lines:
        interpretation['warning'] = "因为有动爻，表示事情正在变化中，需要灵活应对，不可固守成见。"
    else:
        interpretation['warning'] = "卦象相对稳定，但也要注意外界环境的变化。"
    
    # 文化注释
    interpretation['cultural_notes'] = [
        "《易经》强调变化之道，卦象反映的是当前状态和趋势，而非固定命运。",
        "卦辞源于周文王，彖辞、象辞为孔子及其弟子所作，蕴含深刻哲学思想。",
        "解卦时应结合自身实际情况，不可机械套用卦辞爻辞。"
    ]
    
    return interpretation

@app.route('/health')
def health():
    """
    健康检查接口
    """
    return jsonify({'status': 'healthy', 'guas_loaded': len(yijing.gua_data)})

# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                         page_title='页面未找到',
                         error_message='您访问的页面不存在'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                         page_title='服务器错误',
                         error_message='服务器内部错误，请稍后重试'), 500

if __name__ == '__main__':
    # 开发环境配置
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'yijing-opencode-secret-key'
    
    # 确保模板和静态文件目录存在
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("易镜服务启动中...")
    print(f"数据加载完成：{len(yijing.gua_data)} 卦")
    print("访问地址：http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5001, debug=True)