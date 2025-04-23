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
    ("单人模式", "PK模式")
)

# --------- 关键修改区 -----------
# 保留“current_mode”等变量，只清空其它
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
elif mode != st.session_state.current_mode:
    # 模式变化，仅清除业务相关变量，保留current_mode（和need_rerun，如果有）
    for k in list(st.session_state.keys()):
        if k not in ["current_mode", "need_rerun"]:
            del st.session_state[k]
    st.session_state.need_rerun = True
    st.session_state.current_mode = mode

# rerun时保留状态，只执行一次
if st.session_state.get("need_rerun", False):
    st.session_state.need_rerun = False  # 必须重置，否则死循环
    st.rerun()
# --------- 修改区结束 -----------

@st.cache_resource
def init_agent():
    return TurtleSoupAgent()

@st.cache_resource
def init_player_agent():
    return PlayerAgent()

agent = init_agent()
player_agent = init_player_agent()

# ...此处接下来的solo_mode()和pk_mode()部分保持你的逻辑不变
# （与上条Answer一致）

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

    if prompt := st.chat_input("你："):
        st.session_state.pk_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("AI助手思考中..."):
            agent_response = agent.chat(prompt)["message"]
            st.session_state.pk_messages.append({"role": "assistant", "content": agent_response})
            with st.chat_message("assistant"):
                st.markdown(agent_response)
            player_agent.receive_info(agent.memory.to_player_agent())
            player_response = player_agent.answer()
            st.session_state.pk_messages.append({"role": "player", "content": player_response})
            with st.chat_message("player"):
                st.markdown(player_response)
            ai_reply_to_player = agent.chat(player_response)["message"]
            st.session_state.pk_messages.append({"role": "assistant", "content": ai_reply_to_player})
            with st.chat_message("assistant"):
                st.markdown(ai_reply_to_player)
            player_agent.receive_info(agent.memory.to_player_agent())

if mode == "单人模式":
    solo_mode()
elif mode == "PK模式":
    pk_mode()