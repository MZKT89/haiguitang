import streamlit as st
from haiguitangAgent import TurtleSoupAgent

# 设置页面配置
st.set_page_config(
    page_title="海龟汤问答助手",
    page_icon="🐢",
    layout="centered"
)

# 初始会话相关的session_state变量，避免AttributeError
for key, default_text in [
    ("current_story", ""), ("current_truth", ""), ("current_known_info", ""),
    ("show_story", False), ("show_truth", False), ("show_info", False)
]:
    if key not in st.session_state:
        st.session_state[key] = default_text

# 初始化问答Agent
@st.cache_resource
def init_agent():
    return TurtleSoupAgent()

agent = init_agent()

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "您好！我是海龟汤助手，请问您想体验什么类型的海龟汤~"
    })

# 显示历史对话
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # 获取回答和相关信息
    with st.spinner("正在思考，请稍候..."):
        try:
            response = agent.chat(prompt)["message"]
            st.session_state.current_story = agent.memory.get_story() or ""
            st.session_state.current_truth = agent.memory.get_truth() or ""
            st.session_state.current_known_info = agent.memory.get_user_known_info() or ""
        except Exception as e:
            response = f"获取回答时出错：{str(e)}"
    # 添加助手回复
    st.session_state.messages.asppend({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# 固定底部按钮
button_container = st.container()
with button_container:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 故事背景", key="story_button"):
            st.session_state.show_story = not st.session_state.show_story
    with col2:
        if st.button("🔍 事件真相", key="truth_button"):
            st.session_state.show_truth = not st.session_state.show_truth
    with col3:
        if st.button("💡 已知信息", key="info_button"):
            st.session_state.show_info = not st.session_state.show_info

# 显示消息框，内容为空时显示“无”
if st.session_state.show_story:
    with st.expander("📖 故事背景", expanded=True):
        content = st.session_state.current_story.strip() or "无"
        st.markdown(content)

if st.session_state.show_truth:
    with st.expander("🔍 事件真相", expanded=True):
        content = st.session_state.current_truth.strip() or "无"
        st.markdown(content)

if st.session_state.show_info:
    with st.expander("💡 已知信息", expanded=True):
        content = st.session_state.current_known_info.strip() or "无"
        st.markdown(content)