# 易镜 · 模拟周易筮占系统
🪞 基于观测者效应的易经模拟筮占

## 项目简介
本软件是一款基于《周易》六十四卦文本的开源占卜模拟器。我们无意于宣扬迷信，而是旨在提供一种心理学与哲学上的自省工具。软件内置了「观测者效应」理论提示，提醒每一位使用者：心念动处，卦象已成，吉凶悔吝，皆由心生。

## ✨ 功能特点
- **完整《周易》文本**：包含《彖传》、《象传》、《文言传》（部分）及全部爻辞
- **模拟大衍筮法**：还原古法概率分布，支持本卦与变卦的推演
- **观测者效应警示**：每次占卜均附有科学哲学提示，帮助理性看待结果
- **卦象检索系统**：提供完整的六十四卦浏览与查询功能
- **Docker 一键部署**：无需配置 Python 环境，跨平台运行
- **全中文代码注释**：便于学习与二次开发

## 🐳 快速开始 (Docker)

### 1. 克隆项目并进入目录
```bash
git clone <your-repo-url>
cd yijing-opencode
```

### 2. 启动容器
```bash
docker-compose up -d
```

### 3. 访问浏览器
打开浏览器访问：http://localhost:5080

## ⚙️ 本地开发运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行开发服务器
```bash
cd app
python main.py
```

### 3. 访问应用
打开浏览器访问：http://localhost:5000

## 📁 项目结构
```
yijing-opencode/
├── Dockerfile                # Docker容器配置
├── docker-compose.yml        # Docker编排配置
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明文档
├── data/                     # 数据目录
│   └── yijing_full.md        # 易经全文 (UTF-8编码)
├── scripts/                  # 脚本目录
│   └── parse_markdown.py     # Markdown解析脚本
├── app/                      # 主应用目录
│   ├── __init__.py
│   ├── main.py              # Flask主路由
│   ├── yijing_core.py       # 易经核心逻辑类
│   ├── static/              # 静态资源
│   │   ├── css/
│   │   │   └── style.css    # 样式表
│   │   └── js/
│   │       └── main.js      # 前端交互脚本
│   └── templates/           # HTML模板
│       ├── index.html       # 首页 (起卦)
│       ├── result.html      # 解卦结果页
│       └── search.html      # 卦象直查页
└── instance/                # 实例数据
    └── data/
        └── yijing_data.json # 解析后的结构化数据
```

## 🔧 数据预处理
项目包含易经文本解析脚本，可将Markdown格式的易经全文转换为结构化JSON：

```bash
python scripts/parse_markdown.py data/yijing_full.md instance/data/yijing_data.json
```

## 🌐 API接口
应用提供以下REST API接口：

- `GET /` - 首页
- `POST /divinate` - 起卦接口
- `GET /search` - 卦象检索页面
- `GET /api/guas` - 获取所有卦列表 (JSON)
- `GET /api/gua/<id>` - 获取指定卦详情 (JSON)
- `GET /health` - 健康检查接口

## 🎨 界面特色
- **太极动画**：首页包含旋转的太极图动画
- **爻象展示**：使用Unicode符号清晰展示六爻
- **响应式设计**：适配桌面端和移动端
- **古风配色**：玄黑、素白、朱砂红为主色调

## 📜 数据来源
本软件依据《周易》通行本文本整理。文本内容存放于 `data/` 目录下。本项目使用的易经文本为演示版，包含完整的前几卦和最后一卦，实际应用时可替换为完整的六十四卦文本。

## ⚠️ 免责声明
本工具生成的卦象及卦辞解释基于随机算法生成，仅供娱乐与学习传统文化之用。人生重大决策，请务必遵循科学理性与法律法规。

**量子易理提示**：
根据现代物理学中的「观测者效应」，系统在为您生成卦象的瞬间，已干预了原本叠加态的「可能性云」。此卦象是您当前心念与算法随机性共同作用下的「坍缩结果」。
《易》为君子谋，不为小人谋。请将此视为一面镜子，观照内心，而非机械地预测未来。善易者不卜。

## 🤝 贡献指南
欢迎提交Issue和Pull Request来改进本项目。请确保：

1. 保持代码注释为中文
2. 遵循项目的代码风格
3. 更新相关文档

## 📄 许可证
[MIT License](LICENSE)

## 🙏 致谢
- 《周易》文本来源：通行本《周易》
- 设计灵感：量子力学观测者效应
- 开发工具：Flask, Docker, Python

---
**易镜 · 一款有科学态度的易经学习工具**