import os
import openai
import json
from haiguitangAgent.config.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
from haiguitangAgent.Agent.prompt import agent_leaderboard_prompt
from haiguitangAgent.sql_tool.data_utils import read_story_by_id, get_qids
from rich.console import Console
from haiguitangAgent.Memory.Memory import Memory

class TurtleSoupLeaderboardAgent:
    def __init__(self, api_key=OPENAI_API_KEY, model=OPENAI_MODEL, base_url=OPENAI_BASE_URL, q_ids=None):
        if api_key is not None:
            self.api_key = api_key
            # print(f"api_key: {self.api_key}")
        else:
            self.api_key = os.getenv("API_KEY")
        
        if model is not None:
            self.model = model
            # print(f"model: {self.model}")
        else:
            self.model = os.getenv("MODEL")

        if base_url is not None:
            self.base_url = base_url
            # print(f"base_url: {self.base_url}")
        else:
            self.base_url = os.getenv("BASE_URL") 
        self.memory = Memory()
        self.memory.reset()
        self.current_question_index = 0
        self.scores = 0

        # 打榜真题
        # self.question_ids = []
        # question_ids = [2, 5, 7, 8, 9, 10, 14, 34, 62, 88, 228, 291, 345, 2659, 3730, 3731, 3732, 3733, 3734, 3735]
        # for i in q_ids:
        #     self.question_ids.append(question_ids[i-1])
        import random

        # 从1到3735的数字范围
        qids = get_qids()

        # 从nums中随机抽取100个数字
        selected_nums = random.sample(qids, 100)

        self.question_ids = selected_nums

        # TODO 限制论数
        self.left_question_chance = 3  # 每轮游戏的最大问题数
        self.left_answer_chance = 2

        self.finished = False # 打榜过程是否结束
        
        self.messages = [{"role": "system", "content": agent_leaderboard_prompt}] + self.memory.to_messages()

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        # print(f"client: {self.client}")

        self.get_new_game()

    def is_finished(self):
        return self.finished
    
    def get_score(self):
        return f"得分：{self.scores}/{len(self.question_ids)}"
    
    def get_left_question_chance(self):
        return self.left_question_chance
    
    def get_left_answer_chance(self):
        return self.left_answer_chance

    def get_new_game(self):
        """
        获取新的游戏故事和真相
        :param current_question_index: 当前问题索引
        从数据库中获取新的游戏故事和真相
        :return: 新的游戏故事和真相
        """
        self.memory.reset()
        print("==============================================")
        print(f"No.{self.current_question_index+1}")

        story_id = self.question_ids[self.current_question_index]

        story, truth = read_story_by_id(story_id)
        self.memory.store_story_and_truth(story, truth)

        print(f"故事：{story}")
        print(f"真相：{truth}")
        
        self.left_question_chance = 3
        self.left_answer_chance = 2
        self.current_question_index += 1
        
        self.memory.set_left_question_chance(self.left_question_chance)
        self.memory.set_left_answer_chance(self.left_answer_chance)
        self.messages = [{"role": "system", "content": agent_leaderboard_prompt}] + self.memory.to_messages()
        

    def chat(self, question):
        console = Console()
        self.messages.append({"role": "user", "content": question})
        # 修改
        if len(self.messages) >= 20:
            self.messages = self.messages.pop(2) 
        
        try:
            response = self.client.chat.completions.create(
                model = self.model,  
                messages = self.messages,
                response_format = {
                    'type': 'json_object'
                }
            )        
        except Exception as e:
            return "模型调用报错" + str(e)

        if response is None:
            return "模型无响应"
            
        content = response.choices[0].message.content
        if '```json' in content and '```' in content:
        # 去除非 JSON 字符
            content = content.split('```json')[1].split('```')[0].strip()
            try:
                # TODO 判断newgame是不是true，是的话就重置获取新的story， 这里prompt要写返回newgame的条件是上一道题出结果了
                response_data = eval(content)
                
                # TODO 这里改成是否有结果 ，
                bingo = response_data.get("bingo", None)
                # 返回值中没有bingo，说明是一次提问
                if bingo is None:
                    self.left_question_chance -= 1
                else:
                    self.left_answer_chance -= 1

                # 这题结束
                if bingo or self.left_question_chance < 0 or self.left_answer_chance == 0:
                    # TODO 统计结果 对self.scores进行操作
                    if bingo:
                        response = "恭喜你答对了！"
                        self.scores += 1
                    else:
                        response = "未能在限制轮数中揭开谜底~"

                    # 获取新游戏的故事和真相 判断 current question index 
                    if self.current_question_index >= len(self.question_ids):
                        self.finished = True
                        return "打榜完成！"
                    
                    # 获取新的游戏故事和真相
                    self.get_new_game()
                    
                    return response

                elif "user_known_info" in response_data:
                    self.memory.add_user_known_info(response_data["user_known_info"])

                self.memory.set_left_question_chance(self.left_question_chance)
                self.memory.set_left_answer_chance(self.left_answer_chance)
                
                response_message = response_data.get("response_for_user", content)
                return response_message
                
            except json.JSONDecodeError:
                console.print("智能助手的回复不是有效的JSON格式，无法处理。")
        else:
                return content