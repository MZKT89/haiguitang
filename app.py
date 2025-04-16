from haiguitangAgent import TurtleSoupAgent

agent = TurtleSoupAgent()
response = agent.chat("我想玩一个关于校园的游戏")
memory = response["memory"]
print(f"memory: {memory.to_messages()}") 
print(f"外部response: {response}")