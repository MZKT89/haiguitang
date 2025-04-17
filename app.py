from haiguitangAgent import TurtleSoupAgent

agent = TurtleSoupAgent()

while True:
    question = input("请输入问题：")
    response = agent.chat(question)
    # memory = response["memory"]
    # print(f"memory: {memory.to_messages()}") 
    print(f"外部response: {response}")