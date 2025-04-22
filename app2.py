from haiguitangAgent.Agent.PlayerAgent import PlayerAgent
from haiguitangAgent.Agent.Agent_leaderboard import TurtleSoupLeaderboardAgent
import sys

aki_keys = [
    "7d9451a3-d20a-4d51-8294-0ffb01813be0",
    "7d9451a3-d20a-4d51-8294-0ffb01813be0",
    "sk-rrDcSHYLiKNR1NsVcLfQO0qQgs9wMda5Hn7DfAHTrfE3T0On",
    "sk-rrDcSHYLiKNR1NsVcLfQO0qQgs9wMda5Hn7DfAHTrfE3T0On",
    "sk-5b6f757dadf244bfab6e124bb33abf81"
]
models = ["deepseek-r1-250120", "doubao-1-5-thinking-pro-250415", "gpt-3.5-turbo", "gpt-4", "qwen-max"]
base_urls = [
    "https://ark.cn-beijing.volces.com/api/v3",
    "https://ark.cn-beijing.volces.com/api/v3",
    "https://api.chatanywhere.tech/v1",
    "https://api.chatanywhere.tech/v1",
    "https://dashscope.aliyuncs.com/compatible-mode/v1"
]
txt_files = [
    "ds_r1.txt",
    "doubao.txt",
    "gpt35_turbo.txt",
    "gpt4.txt",
    "qwen-max.txt"
]

for i in range(5):
    try:
        aki_key = aki_keys[i]
        model = models[i]
        base_url = base_urls[i]
        with open(txt_files[i], 'a', encoding='utf-8') as f:
            sys.stdout = f

            player_agent = PlayerAgent(aki_key, model, base_url)
            leaderboard_agent = TurtleSoupLeaderboardAgent()

            while not leaderboard_agent.is_finished():
                player_agent.receive_info(leaderboard_agent.memory.to_player_agent())
                player_agent_response = player_agent.answer()
                leaderboard_agent.chat(player_agent_response)

            print(leaderboard_agent.get_score())
    except:
        pass