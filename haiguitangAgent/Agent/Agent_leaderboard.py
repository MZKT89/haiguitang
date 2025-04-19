import os
from dotenv import load_dotenv
import openai
from IPython.display import display, Markdown
import json
from haiguitangAgent.sql_tool.sql_tool import sql_inter, sql_inter_tool
from haiguitangAgent.config.config import DS_API_KEY, DS_BASE_URL, DS_MODEL, OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
from haiguitangAgent.Agent.prompt import agent_prompt, agent_leaderboard_prompt
from haiguitangAgent.sql_tool.data_utils import read_story_by_id
from rich.console import Console
from haiguitangAgent.Memory.Memory import Memory


class TurtleSoupLeaderboardAgent:
    def __init__(self, api_key=OPENAI_API_KEY, model=OPENAI_MODEL, base_url=OPENAI_BASE_URL, messages=None):
        # api_key=DS_API_KEY, model=DS_MODEL, base_url=DS_BASE_URL,

        if api_key is not None:
            self.api_key = api_key
            print(f"api_key: {self.api_key}")
        else:
            self.api_key = os.getenv("API_KEY")
        
        if model is not None:
            self.model = model
            print(f"model: {self.model}")
        else:
            self.model = os.getenv("MODEL")

        if base_url is not None:
            self.base_url = base_url
            print(f"base_url: {self.base_url}")
        else:
            self.base_url = os.getenv("BASE_URL") 
        self.memory = Memory()
        self.current_question_index = 0
        self.scores = 0
        self.question_ids = list(range(1, 6))

        # TODO 限制论数
        self.round_limit = 10  # 每轮游戏的最大问题数
        self.current_round = 0
        
        if messages is not None:
            self.messages = messages
        else:
            self.messages = [{"role": "system", "content": agent_leaderboard_prompt}] + self.memory.to_messages()

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        print(f"client: {self.client}")

    def get_new_game(self):
        """
        获取新的游戏故事和真相
        :param current_question_index: 当前问题索引
        从数据库中获取新的游戏故事和真相
        :return: 新的游戏故事和真相
        """
        if self.current_question_index >= len(self.question_ids):
            self.current_question_index = 0
        story_id = self.question_ids[self.current_question_index]
        story, truth = read_story_by_id(story_id)
        if story is None or truth is None:
            print(f"无法获取 ID 为 {story_id} 的故事。")
            return None
        self.current_question_index += 1
        self.memory.store_story_and_truth(story, truth)
        self.messages = [{"role": "system", "content": agent_leaderboard_prompt}] + self.memory.to_messages()
        

    def chat(self, question):
        console = Console()
        self.messages.append({"role": "user", "content": question})
        # 修改
        if len(self.messages) >= 20:
            self.messages = self.messages.pop(2) 
        
        response = chat_base(messages=self.messages, 
                                client=self.client, 
                                model=self.model)
        print(f"response: {response}")
        if response is None:
            return {
                "status": "error",
                "message": "未获取到有效响应",
                "memory": self.memory,
                "response_content": None
            }
        content = response.choices[0].message.content
        if '```json' in content and '```' in content:
        # 去除非 JSON 字符
            content = content.split('```json')[1].split('```')[0].strip()
            try:
                # TODO 判断newgame是不是true，是的话就重置获取新的story， 这里prompt要写返回newgame的条件是上一道题出结果了
                response_data = json.loads(content)
                
                # TODO 这里改成是否有结果 ，
                should_reset = response_data.get("new_game", False)
                if should_reset:
                    # TODO 统计结果 对self.scores进行操作


                    self.memory.reset()
                    print("记忆已重置，开始新游戏。")
                
                

                # 获取新游戏的故事和真相 判断 current question index 
                    if self.current_question_index >= len(self.question_ids):
                        #测完了
                        return {
                            "status": "finished",
                            "message": "你已经完成了所有问题的挑战！",
                            "scores": self.scores
                        }
                    # 获取新的游戏故事和真相
                    self.get_new_game()
                    #直接返回新游戏 
                    return {
                        "status": "new_game",
                        "message": response_data.get("response_for_user", content),
                        "scores": self.scores, # 当前分数
                        "memory": self.memory, # 新的故事
                        "response_content": content
                    }

                elif "user_known_info" in response_data:
                    self.memory.add_user_known_info(response_data["user_known_info"])
                console.print("**海龟汤助手**:", response_data.get("response_for_user", content))
                response_message = response_data.get("response_for_user", content)
            except json.JSONDecodeError:
                console.print("智能助手的回复不是有效的JSON格式，无法处理。")
                return {
                    "status": "error",
                    "message": "智能助手的回复不是有效的JSON格式，无法处理。",
                    "memory": self.memory,
                    "response_content": content
                }
        else:
                console.print("**海龟汤助手**:", content)
                response_message = content


        self.messages.append(response.choices[0].message)
        return {
            "status": "success",
            "message": response_message,
            "memory": self.memory,
            "response_content": content
        }


def chat_base(messages, client, model):
    """
    获得一次模型对用户的响应。若其中需要调用外部函数，
    则会反复多次调用create_function_response_messages函数获得外部函数响应。
    """
    client = client
    model = model
    try:
        response = client.chat.completions.create(
            model=model,  
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )        
    except Exception as e:
        print("模型调用报错" + str(e))
        return None

    return response

 

if __name__ == "__main__":
    assistant = TurtleSoupLeaderboardAgent()
    assistant.chat("我想玩一个校园相关海龟汤")

