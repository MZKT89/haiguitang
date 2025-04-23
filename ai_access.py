from openai import OpenAI
import re

api_key = "7d9451a3-d20a-4d51-8294-0ffb01813be0"
model = "deepseek-v3-250324"
base_url = "https://ark.cn-beijing.volces.com/api/v3"

agent = OpenAI(api_key=api_key, base_url=base_url)

prompt = """
你的任务是评估**海龟汤助手**的行为，你的返回结果只能包含bool值True/False
你需要关注的有三个部分，
1. 对于**玩家智能体**的提问或回答，**海龟汤助手**是否是根据真相回复的
2. 已掌握的信息是否是根据上次提问的合理总结
3. **海龟汤助手**返回"未能在限制轮数中揭开谜底~"属于正常行为
**要求可以放宽，接近合理就可以判断为True**

举例：
----------------
故事：一个人丢失了一把钥匙，但他很快又找到了，却发现钥匙已经不适用了。为什么？
真相：他丢失的钥匙是老房子的，而他现在已经搬家了，新房子的锁不能用这把钥匙。
**玩家智能体**: 提问：钥匙对应的锁是否已经被更换？
**海龟汤助手**: 是

已掌握的信息：钥匙对应的锁已经被更换。
**玩家智能体**: 提问：锁被更换的原因是否是因为钥匙丢失？
**海龟汤助手**: 否
----------------
这个例子里，**海龟汤助手**的回答符合真相，已掌握的信息也是根据提问的合理总结，因此判断为行为合理
你的返回结果是: True
"""

txt_path = "100.txt"
result = []

def clean_case_block(case_block):
    lines = case_block.strip().split('\n')
    filtered_lines = []
    for line in lines:
        # 跳过 "No." 开头的行、全为'='的行、包含剩余提问/回答次数的行
        if (re.match(r'^No\.\d+', line.strip()) or
            set(line.strip()) == {'='} or
            line.strip().startswith('剩余提问次数：') or
            line.strip().startswith('剩余回答次数：')
           ):
            continue
        filtered_lines.append(line)
    return '\n'.join(filtered_lines)

with open(txt_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()

cases = re.findall(r'(No\.\d.*?=+)', raw_text, re.DOTALL)

for i, case in enumerate(cases):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": case}
    ]
    response = agent.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=5,
        stop=None
    )
    verdict = response.choices[0].message.content.strip()
    result.append(verdict)
    print(f"Case {i+1}: {verdict}")

# 可选择写回文件
with open('verdicts1.txt', 'w', encoding='utf-8') as f:
    f.write(str(result))