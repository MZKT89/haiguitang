import streamlit as st
from haiguitangAgent import TurtleSoupAgent
from haiguitangAgent.Agent.PlayerAgent import PlayerAgent
from haiguitangAgent.Agent.Agent_leaderboard import TurtleSoupLeaderboardAgent

st.set_page_config(
    page_title="海龟汤问答助手",
    page_icon="🐢",
    layout="centered"
)

mode = st.sidebar.selectbox(
    "选择游戏模式",
    ("单人模式", "PK模式", "打榜模式")
)

# ---------- 状态管理 及 刷新逻辑 ----------
SAVED_KEYS = ["current_mode", "need_rerun"]
# 新增通配模式下多余展开状态的key
ALL_MODE_KEYS = [
    "show_story_solo", "show_info_solo",
    "show_story_pk",   "show_info_pk",
    "show_story_lb",   "show_info_lb",
]
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
elif mode != st.session_state.current_mode:
    for k in list(st.session_state.keys()):
        if k not in SAVED_KEYS:
            del st.session_state[k]
    # 二次保险，显式把所有展开按钮状态都清空
    for k in ALL_MODE_KEYS:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.need_rerun = True
    st.session_state.current_mode = mode
if st.session_state.get("need_rerun", False):
    st.session_state.need_rerun = False
    st.rerun()

# ---------- Agent 初始化 ----------
@st.cache_resource
def init_agent():
    return TurtleSoupAgent()

@st.cache_resource
def init_player_agent():
    return PlayerAgent()

@st.cache_resource
def init_leaderboard_agent():
    aki_key = "7d9451a3-d20a-4d51-8294-0ffb01813be0"
    model = "deepseek-v3-250324"
    base_url = "https://ark.cn-beijing.volces.com/api/v3"
    return TurtleSoupLeaderboardAgent(aki_key, model, base_url)

agent = init_agent()
player_agent = init_player_agent()
leaderboard_agent = init_leaderboard_agent()

# ---------- 单人模式 ----------
def solo_mode():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "您好！我是海龟汤助手，请问您想体验什么类型的海龟汤~"
        })

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # prompt输入处理
    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("海龟汤助手思考中，请稍候..."):
            try:
                response = agent.chat(prompt)["message"]
            except Exception as e:
                response = f"获取回答时出错：{str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    # 故事/信息展开配置
    story_key = "show_story_solo"
    info_key = "show_info_solo"
    # 按钮
    button_container = st.container()
    with button_container:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 故事背景", key="btn_story_solo"):
                st.session_state[story_key] = not st.session_state.get(story_key, False)
        with col2:
            if st.button("💡 已知信息", key="btn_info_solo"):
                st.session_state[info_key] = not st.session_state.get(info_key, False)
    # 内容展开
    if st.session_state.get(story_key, False):
        with st.expander("📖 故事背景", expanded=True):
            story = agent.memory.get_story() or "无"
            st.markdown(story)
    if st.session_state.get(info_key, False):
        with st.expander("💡 已知信息", expanded=True):
            known_info = agent.memory.get_user_known_info() or "无"
            st.markdown(known_info)

# ---------- PK 模式 ----------
def pk_mode():
    if "pk_messages" not in st.session_state:
        st.session_state.pk_messages = []
        st.session_state.pk_messages.append({
            "role": "assistant",
            "content": "欢迎进入PK模式！你可以和AI轮流推理。请您先选择海龟汤类型~"
        })
    for message in st.session_state.pk_messages:
        # 玩家AI消息做特殊美化头像
        if message["role"] == "player":
            with st.chat_message("player", avatar="🧑‍💼"): # 可替换emoji或图片链接
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("你："):
        st.session_state.pk_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # 出题AI思考
        with st.spinner("海龟汤助手思考中..."):
            agent_response = agent.chat(prompt)["message"]
        st.session_state.pk_messages.append({"role": "assistant", "content": agent_response})
        with st.chat_message("assistant"):
            st.markdown(agent_response)
        player_agent.receive_info(agent.memory.to_player_agent())
        # 玩家AI思考提示
        with st.spinner("AI玩家思考中..."):
            player_response = player_agent.answer()
        st.session_state.pk_messages.append({"role": "player", "content": player_response})
        with st.chat_message("player", avatar="🧑‍💼"): # 可替换emoji或图片链接
            st.markdown(player_response)
        # 再返回
        ai_reply_to_player = agent.chat(player_response)["message"]
        st.session_state.pk_messages.append({"role": "assistant", "content": ai_reply_to_player})
        with st.chat_message("assistant"):
            st.markdown(ai_reply_to_player)
        player_agent.receive_info(agent.memory.to_player_agent())

    # 故事/信息展开配置
    story_key = "show_story_pk"
    info_key = "show_info_pk"
    button_container = st.container()
    with button_container:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 故事背景", key="btn_story_pk"):
                st.session_state[story_key] = not st.session_state.get(story_key, False)
        with col2:
            if st.button("💡 已知信息", key="btn_info_pk"):
                st.session_state[info_key] = not st.session_state.get(info_key, False)
    if st.session_state.get(story_key, False):
        with st.expander("📖 故事背景", expanded=True):
            story = agent.memory.get_story() or "无"
            st.markdown(story)
    if st.session_state.get(info_key, False):
        with st.expander("💡 已知信息", expanded=True):
            known_info = agent.memory.get_user_known_info() or "无"
            st.markdown(known_info)

# ---------- 打榜模式 ----------
def leaderboard_mode():
    if "lb_messages" not in st.session_state:
        st.session_state.lb_messages = []
        story = leaderboard_agent.memory.get_story()
        user_known_info = leaderboard_agent.memory.get_user_known_info()
        first_msg = "欢迎来到打榜模式！你将和全球玩家同场竞技。"
        st.session_state.lb_messages.append({"role": "assistant", "content": first_msg})
        st.session_state.lb_messages.append({"role": "assistant", "content": f"故事背景：{story}"})

    # 展示历史
    for message in st.session_state.lb_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("请输入你的推理、提问或猜测...")

    if prompt:
        st.session_state.lb_messages.append({"role": "user", "content": prompt})
        st.session_state["pending_lb_prompt"] = prompt
        st.rerun()
        return

    if st.session_state.get("pending_lb_prompt", None):
        pending = st.session_state["pending_lb_prompt"]
        with st.spinner("AI判定中..."):
            response = leaderboard_agent.chat(pending)
            st.session_state.lb_messages.append({
                "role": "assistant",
                "content": f"{response}"
            })
            # 检查是否答对，重新生成story
            if "恭喜你答对了！" or "未能在限制轮数中揭开谜底~" in str(response):
                new_story = leaderboard_agent.memory.get_story()
                st.session_state.lb_messages.append({
                    "role": "assistant",
                    "content": f"新故事背景是：{new_story}"
                })
        del st.session_state["pending_lb_prompt"]
        st.rerun()
        return

    if leaderboard_agent.is_finished():
        score = leaderboard_agent.get_score()
        st.session_state.lb_messages.append({
            "role": "assistant",
            "content": f"🎉 游戏结束！您的推理解谜得分为：**{score}**"
        })
        with st.chat_message("assistant"):
            st.markdown(f"🎉 游戏结束！您的推理解谜得分为：**{score}**")
        if st.button("再来一局", key="lb_restart"):
            for k in list(st.session_state.keys()):
                if k not in SAVED_KEYS:
                    del st.session_state[k]
            for k in ALL_MODE_KEYS:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # 故事和已知信息展开按钮...
    story_key = "show_story_lb"
    info_key = "show_info_lb"
    button_container = st.container()
    with button_container:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 故事背景", key="btn_story_lb"):
                st.session_state[story_key] = not st.session_state.get(story_key, False)
        with col2:
            if st.button("💡 已知信息", key="btn_info_lb"):
                st.session_state[info_key] = not st.session_state.get(info_key, False)
    if st.session_state.get(story_key, False):
        with st.expander("📖 故事背景", expanded=True):
            story = leaderboard_agent.memory.get_story() or "无"
            st.markdown(story)
    if st.session_state.get(info_key, False):
        with st.expander("💡 已知信息", expanded=True):
            known_info = leaderboard_agent.memory.get_user_known_info() or "无"
            st.markdown(known_info)

# ========== 模式路由 ==========
if mode == "单人模式":
    solo_mode()
elif mode == "PK模式":
    pk_mode()
elif mode == "打榜模式":
    leaderboard_mode()