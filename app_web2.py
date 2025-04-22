import streamlit as st
from haiguitangAgent import TurtleSoupAgent
from haiguitangAgent.Agent.PlayerAgent import PlayerAgent

# 页面设置
st.set_page_config(
    page_title="海龟汤问答助手",
    page_icon="🐢",
    layout="centered"
)

# 在侧边栏选择模式
mode = st.sidebar.selectbox(
    "选择游戏模式",
    ("单人模式", "PK智能体")
)

# 模式切换时刷新页面并重置会话
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
elif mode != st.session_state.current_mode:
    # 模式发生切换，重置所有会话状态
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.current_mode = mode
    st.experimental_rerun()

# 初始化 agent
@st.cache_resource
def init_agent():
    return TurtleSoupAgent()

@st.cache_resource
def init_player_agent():
    return PlayerAgent()

agent = init_agent()
player_agent = init_player_agent()

### 单人模式逻辑
def solo_mode():
    # 初始化会话历史
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "您好！我是海龟汤助手，请问您想体验什么类型的海龟汤~"
        })

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 处理输入
    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("正在思考，请稍候..."):
            try:
                response = agent.chat(prompt)["message"]
                st.session_state.current_story = agent.memory.get_story() or ""
                st.session_state.current_truth = agent.memory.get_truth() or ""
                st.session_state.current_known_info = agent.memory.get_user_known_info() or ""
            except Exception as e:
                response = f"获取回答时出错：{str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    # 固定底部按钮
    button_container = st.container()
    with button_container:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📖 故事背景", key="story_button"):
                st.session_state.show_story = not st.session_state.get("show_story", False)
        with col2:
            if st.button("🔍 事件真相", key="truth_button"):
                st.session_state.show_truth = not st.session_state.get("show_truth", False)
        with col3:
            if st.button("💡 已知信息", key="info_button"):
                st.session_state.show_info = not st.session_state.get("show_info", False)

    # 展开信息
    if st.session_state.get("show_story", False):
        with st.expander("📖 故事背景", expanded=True):
            content = st.session_state.get("current_story", "").strip() or "无"
            st.markdown(content)

    if st.session_state.get("show_truth", False):
        with st.expander("🔍 事件真相", expanded=True):
            content = st.session_state.get("current_truth", "").strip() or "无"
            st.markdown(content)

    if st.session_state.get("show_info", False):
        with st.expander("💡 已知信息", expanded=True):
            content = st.session_state.get("current_known_info", "").strip() or "无"
            st.markdown(content)

### PK 智能体模式逻辑
def pk_mode():
    if "pk_messages" not in st.session_state:
        st.session_state.pk_messages = []
        st.session_state.pk_messages.append({
            "role": "assistant",
            "content": "欢迎进入PK模式！你可以和AI轮流推理。请你先提问或猜测。"
        })

    for message in st.session_state.pk_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 输入框
    if prompt := st.chat_input("你："):
        # 用户提问
        st.session_state.pk_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("AI助手思考中..."):
            agent_response = agent.chat(prompt)["message"]
            st.session_state.pk_messages.append({"role": "assistant", "content": agent_response})
            with st.chat_message("assistant"):
                st.markdown(agent_response)
            # AI给player agent信息并作答
            player_agent.receive_info(agent.memory.to_player_agent())
            player_response = player_agent.answer()
            st.session_state.pk_messages.append({"role": "player", "content": player_response})
            with st.chat_message("player"):
                st.markdown(player_response)
            # AI根据player agent猜测回复
            ai_reply_to_player = agent.chat(player_response)["message"]
            st.session_state.pk_messages.append({"role": "assistant", "content": ai_reply_to_player})
            with st.chat_message("assistant"):
                st.markdown(ai_reply_to_player)
            player_agent.receive_info(agent.memory.to_player_agent())

# 主体部分
if mode == "单人模式":
    solo_mode()
elif mode == "PK智能体":
    pk_mode()