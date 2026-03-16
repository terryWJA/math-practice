# 加减法算术练习

一个简洁美观的 Web 版加减法练习工具，支持 PC 和移动端自动适配。

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 功能特性

- ✅ 题目数量自由设置（5-30 道）
- ✅ 最大数字范围可选（10-100）
- ✅ 支持加法、减法运算
- ✅ 三种难度：简单（2个数）、中等（3个数）、困难（4个数）
- ✅ 答题即时检查与统计
- ✅ PC / 移动端自动适配

## 本地运行

```bash
# 克隆项目
git clone https://github.com/terryWJA/math-practice.git
cd math-practice

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

打开浏览器访问 http://localhost:5000

## 项目结构

```
math-practice/
├── app.py              # Flask 主程序
├── requirements.txt   # Python 依赖
├── sum.html           # 原版 HTML（参考）
└── templates/
    ├── index.html     # PC 端页面
    └── mobile.html    # 移动端页面
```

## 技术栈

- **后端**：Flask
- **前端**：HTML + TailwindCSS + Vanilla JS

## License

MIT
