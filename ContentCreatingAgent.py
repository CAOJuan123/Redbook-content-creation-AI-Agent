import streamlit as st
import requests
import json

# 你的通义千问密钥
DASHSCOPE_API_KEY = "sk-XXXXXXX"

# 页面全局美化配置
st.set_page_config(
    page_title="小红书爆款文案智能Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义页面样式美化
st.markdown("""
<style>
.main {background-color: #f9f5f6;}
.stTabs [data-baseweb="tab"] {font-size:16px; font-weight:bold;}
.stButton>button {border-radius:8px;}
.stTextArea>div>textarea {border-radius:8px;}
.stTextInput>div>input {border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# 初始化历史记录
if "history_list" not in st.session_state:
    st.session_state.history_list = []

# 通用调用通义千问
def qwen_call(prompt, temp=0.92):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"temperature": temp, "top_p": 0.95}
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    return res.json()["output"]["text"]

# 拼接字数+语气约束
def get_len_tone_rule(len_mode, tone_mode):
    len_rule = {
        "精简短句版":"篇幅短小精炼，字数少，适合快速阅读",
        "标准小红书版":"常规适中篇幅，标准笔记长度",
        "长篇深度种草版":"内容详细，细节丰富，长篇走心种草"
    }[len_mode]

    tone_rule = {
        "温柔治愈":"语气柔和、细腻暖心",
        "日常闺蜜":"像和闺蜜聊天，自然接地气",
        "夸张发疯":"情绪饱满、感叹多、活泼种草感强",
        "强带货营销":"种草安利感直接，说服力强"
    }[tone_mode]

    return len_rule, tone_rule

# 1. 自定义风格生成文案 + 防幻觉
def generate_custom_copy(brand, industry, user_style, topic, len_mode, tone_mode):
    len_rule, tone_rule = get_len_tone_rule(len_mode, tone_mode)
    prompt = f"""
你是资深小红书爆款博主，创作种草文案，严格遵守所有规则，禁止编造不存在内容：

品牌：{brand}
所属行业：{industry}
指定风格：{user_style}
笔记主题：{topic}
篇幅要求：{len_rule}
语气人设：{tone_rule}

核心硬性规则：
1. 只基于用户提供的品牌、行业、主题、风格创作，**严禁编造未提及的IP、产品、周边、赠品**；
2. 可描述通用特点，禁止私自编造具体产品名称，除非用户主题里明确给出；
3. 紧扣主题不跑偏，不延伸无关内容；
4. 小红书爆款结构：吸睛标题+情绪开头+真实体验+种草收尾；
5. 短句分行、排版清爽、emoji适量；
6. 真人语气无AI味、无官方话术；
7. 结尾只生成**4个精准不重复垂直标签**，不多不少、不冗余。

直接输出成品文案，不要多余解释。
"""
    return qwen_call(prompt)

# 2. 竞品分析 + 高阶仿写 防幻觉
def analyze_and_high_level_imitate(competitor_text, brand, industry, user_style, topic, len_mode, tone_mode):
    analyze_prompt = f"""
深度拆解这篇小红书爆款文案，只提炼骨架风格，不要复述全文：
1.标题句式结构 2.开头情绪钩子类型 3.正文段落逻辑
4.整体语感人设 5.emoji与排版习惯 6.标签搭配思路
简洁分点说明：
{competitor_text}
"""
    analysis = qwen_call(analyze_prompt, 0.85)

    len_rule, tone_rule = get_len_tone_rule(len_mode, tone_mode)
    rewrite_prompt = f"""
严格高阶仿写：只模仿参考文案的标题结构、开头钩子、语气人设、段落节奏、排版风格，
**禁止整句照抄、禁止只改品牌名、禁止编造不存在内容**，完全原创适配我方品牌。

参考爆款文案：
{competitor_text}

我方信息：
品牌：{brand}
行业：{industry}
指定风格：{user_style}
创作主题：{topic}
篇幅要求：{len_rule}
语气人设：{tone_rule}

硬性规则：
1.仅基于用户给定信息创作，不私自加IP、产品、周边；
2.保持小红书排版，emoji适量；
3.语气贴合指定人设，无机器味；
4.结尾严格只给4个精准不重复专属标签。

直接输出仿写原创文案，不要解释。
"""
    new_copy = qwen_call(rewrite_prompt)
    return analysis, new_copy

# 3. 文案多版本润色衍生
def rewrite_multi_version(origin_text):
    prompt = f"""
请把下面这篇小红书文案，衍生出4个不同版本，每个版本独立成篇：
1.精简干练版 2.温柔氛围感版 3.活泼接地气版 4.高级冷淡质感版
保持核心意思不变，只改语气和措辞，每篇结尾带合适标签。
原文案：
{origin_text}
"""
    return qwen_call(prompt)

# 一键清空所有输入
def reset_all():
    st.session_state.brand = ""
    st.session_state.industry = ""
    st.session_state.user_style = ""
    st.session_state.topic = ""
    st.session_state.competitor_text = ""

# 侧边栏
with st.sidebar:
    st.title("✨ 文案Agent控制台")
    st.header("📝 基础信息")
    brand = st.text_input("你的品牌名称", key="brand", placeholder="输入自有品牌")
    industry = st.selectbox("所属行业", key="industry", options=[
        "美妆护肤","茶饮奶茶","服饰穿搭","咖啡甜品",
        "家居好物","香氛配饰","日用百货"
    ])
    user_style = st.text_input("自定义文案风格", key="user_style", placeholder="韩系温柔/ins风/平价接地气")
    topic = st.text_input("笔记创作主题", key="topic", placeholder="夏日限定/IP联名周边/无限回购")

    st.divider()
    st.header("⚙️ 生成参数设置")
    len_mode = st.selectbox("文案篇幅档位", options=["精简短句版","标准小红书版","长篇深度种草版"])
    tone_mode = st.selectbox("语气人设档位", options=["温柔治愈","日常闺蜜","夸张发疯","强带货营销"])

    st.divider()
    if st.button("🔄 一键清空所有输入", type="secondary"):
        reset_all()

    st.divider()
    st.header("📜 历史生成记录")
    for idx, item in enumerate(st.session_state.history_list[-10:]):
        with st.expander(f"记录{idx+1}｜{item['title']}"):
            st.markdown(item["content"])
            st.text_area("复制", item["content"], height=180)

# 主标题
st.title("✨ 小红书爆款文案智能Agent｜自定义生成+竞品高阶仿写")
st.divider()

tab1, tab2, tab3 = st.tabs(["✨ 自定义风格生成", "🔍 竞品爆款高阶仿写", "🔄 文案多版本润色"])

# Tab1 自定义生成
with tab1:
    st.subheader("✨ 按自定义风格一键生成原创文案")
    if st.button("🚀 生成原创文案", type="primary"):
        if not brand or not topic or not user_style:
            st.warning("⚠️ 请填写品牌、自定义风格、创作主题！")
        else:
            with st.spinner("智能生成中，请稍候…"):
                res = generate_custom_copy(brand, industry, user_style, topic, len_mode, tone_mode)
            st.markdown("### ✅ 生成成品文案")
            st.markdown(res)
            st.text_area("📋 一键复制文案", res, height=300)
            # 存入历史记录
            st.session_state.history_list.append({"title":topic, "content":res})

# Tab2 竞品仿写
with tab2:
    st.subheader("🔍 粘贴竞品文案 → 风格拆解 + 原创高阶仿写")
    st.info("💡 仅模仿结构语气，不照抄、不编造无关内容")
    competitor_text = st.text_area("粘贴小红书竞品整篇爆款文案", key="competitor_text", height=280)
    if st.button("🚀 拆解并高阶仿写", type="primary"):
        if not competitor_text or not brand or not topic or not user_style:
            st.warning("⚠️ 请填全基础信息并粘贴竞品文案！")
        elif len(competitor_text.strip()) < 50:
            st.warning("⚠️ 竞品文案过短，无法有效分析仿写，请粘贴完整笔记！")
        else:
            with st.spinner("拆解爆款逻辑 + 原创仿写中…"):
                analysis, new_copy = analyze_and_high_level_imitate(competitor_text, brand, industry, user_style, topic, len_mode, tone_mode)
            st.markdown("### 📊 竞品爆款风格拆解")
            st.markdown(analysis)
            st.divider()
            st.markdown("### ✍️ 仿写原创文案（同风格不照抄）")
            st.markdown(new_copy)
            st.text_area("📋 一键复制仿写文案", new_copy, height=300)
            st.session_state.history_list.append({"title":"竞品仿写-"+topic, "content":new_copy})

# Tab3 文案多版本润色
with tab3:
    st.subheader("🔄 输入已有文案，一键衍生4种风格版本")
    origin_text = st.text_area("粘贴你要改写的原文案", height=280)
    if st.button("🚀 一键多版本衍生", type="primary"):
        if not origin_text.strip():
            st.warning("⚠️ 请粘贴需要改写的原文案！")
        else:
            with st.spinner("多风格改写中…"):
                multi_res = rewrite_multi_version(origin_text)
            st.markdown("### ✅ 4种风格衍生文案")
            st.markdown(multi_res)
            st.text_area("📋 全部复制", multi_res, height=350)
            st.session_state.history_list.append({"title":"多版本改写", "content":multi_res})
