from haiguitangAgent import TurtleSoupAgent
from haiguitangAgent.Agent.PlayerAgent import PlayerAgent

agent = TurtleSoupAgent()
player_agent = PlayerAgent()

while True:
    question = input("请输入问题：")
    response = agent.chat(question)
    # memory = response["memory"]
    # print(f"memory: {memory.to_messages()}") 
    print(f"**出题Agent**: {response}")

    player_agent.receive_info(agent.response)
    player_agent_response = player_agent.answer()
    response_to_player_agent = agent.chat(player_agent_response)
    print(f"**出题Agent**: {response_to_player_agent}")

    player_agent.receive_info(agent.response)