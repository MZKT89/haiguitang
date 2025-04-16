from haiguitangAgent import TurtleSoupAgent

agent = TurtleSoupAgent()
response = agent.chat("我想玩一个校园相关的游戏")
memory = response["memory"]
print(f"memory: {memory.to_messages()}") 
print(f"外部response: {response}")