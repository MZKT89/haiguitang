from haiguitangAgent.Agent.PlayerAgent import PlayerAgent
from haiguitangAgent.Agent.Agent_leaderboard import TurtleSoupLeaderboardAgent
import sys

q_ids = [
    [13, 17, 18, 20],
    [7, 17, 19],
    [3, 4, 12, 17, 20], 
    [2, 9, 17,18], 
    [1, 2, 3, 10, 15]
]

aki_keys = [
    "7d9451a3-d20a-4d51-8294-0ffb01813be0",
    "7d9451a3-d20a-4d51-8294-0ffb01813be0",
    "sk-rrDcSHYLiKNR1NsVcLfQO0qQgs9wMda5Hn7DfAHTrfE3T0On",
    "sk-rrDcSHYLiKNR1NsVcLfQO0qQgs9wMda5Hn7DfAHTrfE3T0On",
    "sk-5b6f757dadf244bfab6e124bb33abf81",
    "sk-e8xEJFpNQDD6Yrxc0c282e1416264c21943405C4C49419Bc",
    "sk-e8xEJFpNQDD6Yrxc0c282e1416264c21943405C4C49419Bc"
]
models = [
    "deepseek-r1-250120", 
    "doubao-1-5-thinking-pro-250415", 
    "gpt-3.5-turbo", 
    "gpt-4", 
    "qwen-max",
    "claude-3-5-sonnet-all",
    "gemini-2.0-flash"
]
base_urls = [
    "https://ark.cn-beijing.volces.com/api/v3",
    "https://ark.cn-beijing.volces.com/api/v3",
    "https://api.chatanywhere.tech/v1",
    "https://api.chatanywhere.tech/v1",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "https://api.gpt.ge/v1/",
    "https://api.gpt.ge/v1/"
]
txt_files = [
    "ds_r1_.txt",
    "doubao_.txt",
    "gpt35_turbo_.txt",
    "gpt4_.txt",
    "qwen-max_.txt",
    "claude-3-5-sonnet-all.txt",
    "gemini-2.0-flash.txt"
]
i=1
aki_key = aki_keys[i]
model = models[i]
base_url = base_urls[i]
# q_id = q_ids[i]
with open('100.txt', 'a', encoding='utf-8') as f:
    sys.stdout = f

    player_agent = PlayerAgent(aki_key, model, base_url)
    leaderboard_agent = TurtleSoupLeaderboardAgent()

    while not leaderboard_agent.is_finished():
        player_agent.receive_info(leaderboard_agent.memory.to_player_agent())
        player_agent_response = player_agent.answer()
        leaderboard_agent.chat(player_agent_response)

    print(leaderboard_agent.get_score())
# for i in range(5):
    # try:
    #     aki_key = aki_keys[i]
    #     model = models[i]
    #     base_url = base_urls[i]
    #     q_id = q_ids[i]
    #     with open(txt_files[i], 'a', encoding='utf-8') as f:
    #         sys.stdout = f

    #         player_agent = PlayerAgent(aki_key, model, base_url)
    #         leaderboard_agent = TurtleSoupLeaderboardAgent(q_ids=q_id)

    #         while not leaderboard_agent.is_finished():
    #             player_agent.receive_info(leaderboard_agent.memory.to_player_agent())
    #             player_agent_response = player_agent.answer()
    #             leaderboard_agent.chat(player_agent_response)

    #         print(leaderboard_agent.get_score())
    # except:
    #     pass