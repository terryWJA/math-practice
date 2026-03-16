from flask import Flask, render_template, request, jsonify, make_response
from fpdf import FPDF
import random
import re
import io

app = Flask(__name__)

def is_mobile(user_agent):
    """根据 User-Agent 判断是否为移动设备"""
    patterns = [
        r'Android', r'webOS', r'iPhone', r'iPad', r'iPod',
        r'BlackBerry', r'IEMobile', r'Opera Mini', r'Mobile',
        r'Tablet', r'Nexus', r'Mobile Safari'
    ]
    return any(re.search(p, user_agent, re.I) for p in patterns)

def generate_problem(max_num, allow_add, allow_sub, segments):
    """生成一道算术题"""
    operators = []
    if allow_add:
        operators.append('+')
    if allow_sub:
        operators.append('-')
    
    if not operators:
        return None
    
    numbers = []
    ops = []
    result = 0
    attempts = 0
    
    while attempts < 100:
        numbers = []
        ops = []
        current = random.randint(1, max_num - 1)
        numbers.append(current)
        result = current
        valid = True
        
        for _ in range(segments - 1):
            op = random.choice(operators)
            
            if op == '+':
                next_num = random.randint(1, max_num - result)
                if result + next_num > max_num:
                    valid = False
                result += next_num
            else:
                if result <= 1:
                    valid = False
                    next_num = 0
                else:
                    next_num = random.randint(1, result)
                    result -= next_num
            
            if result < 0 or result > max_num:
                valid = False
            
            ops.append(op)
            numbers.append(next_num)
        
        if valid and 0 <= result <= max_num:
            break
        attempts += 1
    
    if attempts >= 100:
        return generate_problem(max_num, allow_add, allow_sub, segments)
    
    return {'numbers': numbers, 'operators': ops, 'answer': result}

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '')
    if is_mobile(user_agent):
        return render_template('mobile.html')
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    count = data.get('count', 10)
    max_num = data.get('maxNum', 50)
    allow_add = data.get('allowAdd', True)
    allow_sub = data.get('allowSub', True)
    segments = data.get('segments', 3)
    
    problems = []
    for _ in range(count):
        problem = generate_problem(max_num, allow_add, allow_sub, segments)
        if problem:
            problems.append(problem)
    
    return jsonify({'problems': problems})

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    """导出题目为 PDF"""
    data = request.json
    problems = data.get('problems', [])
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Math Practice', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f'Problems: {len(problems)}', ln=True)
    pdf.ln(5)
    
    # 题目区域
    pdf.set_font("Arial", 'B', 14)
    col_width = 90
    row_height = 10
    x_start = 10
    
    for i, p in enumerate(problems):
        if i % 2 == 0:
            pdf.set_x(x_start)
        
        # 构建题目表达式
        expr = str(p['numbers'][0])
        for j, op in enumerate(p['operators']):
            expr += f' {op} {p["numbers"][j+1]}'
        expr += ' ='
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(col_width, row_height, f'{i+1}. {expr}', border=0)
        
        if i % 2 == 1:
            pdf.ln()
    
    # 答案区域
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Answers', ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    for i, p in enumerate(problems):
        if i % 4 == 0:
            if i > 0:
                pdf.ln()
            pdf.set_x(x_start)
        pdf.cell(40, 8, f'{i+1}. {p["answer"]}', border=0)
    pdf.ln()
    
    # 答题区域
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Work Area', ln=True)
    pdf.ln(5)
    
    for i in range(len(problems)):
        if i % 2 == 0:
            pdf.set_x(x_start)
        pdf.cell(col_width, 15, '', border=1)
        if i % 2 == 1:
            pdf.ln()
    
    # 输出 PDF
    pdf_data = pdf.output()
    if isinstance(pdf_data, (bytearray, str)):
        pdf_data = bytes(pdf_data)
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=math-practice.pdf'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
