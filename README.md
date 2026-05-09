小红书爆款文案智能Agent


🤖 基于Python+通义千问API的垂直场景AI Agent，专注小红书内容营销创作
✨ 项目简介


独立设计并落地的垂直场景AI Agent，核心解决内容营销场景下的文案创作效率问题。


核心技术亮点：防幻觉机制设计


V1版本遇到问题：AI会"自由发挥"，编造不存在的产品/IP/赠品
V2版本解决方案：四层防幻觉约束体系，文案原创度95%+
🎯 核心功能


功能	说明
✨ 自定义风格生成	输入品牌+行业+风格，一键生成原创爆款文案
🔍 竞品分析+高阶仿写	拆解竞品爆款骨架，生成原创仿写文案
🔄 多版本润色	一篇文案衍生4种风格变体
🛠️ 技术栈


语言：Python 3.x
前端：Streamlit
AI服务：通义千问API (qwen-turbo)
核心能力：提示词工程、防幻觉优化、Agent设计
📂 项目结构


plaintext
├── ContentCreatingAgent.py    # 核心Agent代码
├── README.md                  # 项目文档
└── screenshots/               # 产品截图

🔒 防幻觉机制（核心亮点）
V1版本问题


❌ AI编造不存在的周边产品（用户只输入HelloKitty联名，AI生成"小熊钥匙扣+贴纸+手账本"）
V2解决方案：四层约束体系


层级	设计	作用
第1层	角色设定+信息注入	明确AI的"素材库"范围
第2层	核心硬性规则	"严禁编造未提及的IP、产品、周边"
第3层	正向引导规范	告诉AI应该怎么做
第4层	输出格式约束	固定结构，减少自由度
硬性规则示例


plaintext
核心硬性规则：
1. 只基于用户提供的品牌、行业、主题、风格创作，**严禁编造未提及的IP、产品、周边、赠品**
2. 可描述通用特点，禁止私自编造具体产品名称，除非用户主题里明确给出
3. 紧扣主题不跑偏，不延伸无关内容

📊 效果展示
自定义风格生成


竞品分析+高阶仿写


多版本润色


🚀 快速上手
环境要求


Python 3.x
通义千问API Key
安装运行


bash
# 1. 克隆项目
git clone https://github.com/CAOJuan123/Redbook-content-creation-AI-Agent.git
cd Redbook-content-creation-AI-Agent

# 2. 安装依赖
pip install streamlit requests

# 3. 配置API Key
# 编辑 ContentCreatingAgent.py，替换 DASHSCOPE_API_KEY 为你的API Key

# 4. 运行
streamlit run ContentCreatingAgent.py

📌 未来优化方向


对话式优化：支持多轮指令调整
品牌知识库：上传品牌资料，生成更贴合的内容
违禁词检测：接入广告法违禁词API
多平台适配：支持抖音、微博等平台文案风格
👤 关于作者
求职意向：AI产品经理 / AI Agent工程师
教育背景：香港城市大学 理学硕士（商业信息系统）
技能：AI Agent设计、提示词工程、防幻觉优化

📧 2767113138@qq.com# 
