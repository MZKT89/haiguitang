from haiguitangAgent import TurtleSoupAgent
from haiguitangAgent.Agent.PlayerAgent import PlayerAgent

agent = TurtleSoupAgent()
player_agent = PlayerAgent()

while True:
    question = input("请输入问题：")
    response = agent.chat(question)
    print(f"**海龟汤助手**: {response}")

    player_agent.receive_info(agent.memory.to_player_agent())
    player_agent_response = player_agent.answer()
    print(f"**玩家智能体**: {player_agent_response}")

    response_to_player_agent = agent.chat(player_agent_response)
    print(f"**海龟汤助手**: {response_to_player_agent}")

    player_agent.receive_info(agent.memory.to_player_agent())

# while True:
#     question = input("请输入问题：")
#     response = agent.chat(question)
#     print(f"**出题Agent**: {response}")

#     player_agent.receive_info(agent.memory.get_story(), agent.memory.get_user_known_info())
#     player_agent_response = player_agent.answer()
#     response_to_player_agent = agent.chat(player_agent_response)
#     print(f"**出题Agent**: {response_to_player_agent}")

#     player_agent.receive_info(agent.memory.get_story(), agent.memory.get_user_known_info())