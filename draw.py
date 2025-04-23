import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 定义数据
data = {
    'Model': ['doubao1.5-thinking-pro', 'deepseek-r1', 'gpt4', 'claude3.5-sonnet-all', 'gpt3.5-turbo', 'qwen-max', 'gemini2.0-flash'],
    'Accuracy': [13 / 20, 10 / 20, 9 / 20, 8 / 20, 7 / 20, 7 / 20, 7 / 20]
}

# 创建 DataFrame
df = pd.DataFrame(data)

# 设置 Streamlit 页面
# st.title('不同模型得分对比柱状图')

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 创建画布
plt.figure(figsize=(10, 6))

# 使用 seaborn 绘制横向柱状图
sns.barplot(x='Accuracy', y='Model', data=df, palette='viridis')

# 添加数据标签，并设置字体大小
for i, v in enumerate(df['Accuracy']):
    plt.text(v + 0.01, i, f'{round(v, 2)}', va='center', fontsize=14)

# 设置模型名称字号
plt.yticks(fontsize=16)

# 设置图表标题和坐标轴标签，同时调大字号
plt.title('Comparison of Accuracy of Player Agents Using Different Models', fontsize=20, fontweight='bold', y=1.05)
plt.xlabel('Accuracy', fontsize=18)
plt.xticks(rotation=45, fontsize=14)
plt.ylabel('Model', fontsize=18)

# 设置横坐标最大值为 1
plt.xlim(0, 1)

# 显示网格线
plt.grid(True, axis='x')

# 显示图表
st.pyplot(plt)
    