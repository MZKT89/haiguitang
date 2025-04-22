import os
import openai
from haiguitangAgent.config.config import PLAYER_AGENT_API_KEY, PLAYER_AGENT_BASE_URL, PLAYER_AGENT_MODEL
from haiguitangAgent.Agent.prompt import player_agent_prompt

class PlayerAgent:
    def __init__(self, api_key=PLAYER_AGENT_API_KEY, model=PLAYER_AGENT_MODEL, base_url=PLAYER_AGENT_BASE_URL):
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

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        # print(f"client: {self.client}")
        # self.memory = PlayerMemory()

    def receive_info(self, info):
        self.messages = [{"role": "system", "content": player_agent_prompt}]
        if story := info.get("story", None):
            print(f"故事：{story}")
            self.messages.append({"role": "user", "content": "题目：" + story})
        if truth := info.get("truth", None):
            print(f"真相：{truth}")
        if user_known_info := info.get("user_known_info", None):
            print(f"已掌握的信息：{user_known_info}")
            self.messages.append({"role": "user", "content": "已掌握的信息：" + user_known_info})
        if left_question_chance := info.get("left_question_chance", None):
            print(f"剩余提问次数：{left_question_chance}")
            self.messages.append({"role": "user", "content": "剩余提问次数：" + left_question_chance})
        if left_answer_chance := info.get("left_answer_chance", None):
            print(f"剩余回答次数：{left_answer_chance}")
            self.messages.append({"role": "user", "content": "剩余回答次数：" + left_answer_chance})

    def answer(self):
        try:
            if not self.messages:
                return
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            answer = response.choices[0].message.content
            answer = answer.strip()
            print(f"**玩家智能体**: {answer}")
            return answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

