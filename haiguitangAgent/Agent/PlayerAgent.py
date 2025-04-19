import os
import openai
import json
from haiguitangAgent.config.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from haiguitangAgent.Agent.prompt import player_agent_prompt
from rich.console import Console
from haiguitangAgent.Memory.Memory import Memory


class PlayerAgent:
    def __init__(self, api_key=OPENAI_API_KEY, model=OPENAI_MODEL, base_url=OPENAI_BASE_URL, messages=None):
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
            
        if messages is not None:
            self.messages = messages
        else:
            self.messages = [{"role": "system", "content": player_agent_prompt}]

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        print(f"client: {self.client}")
        # self.memory = PlayerMemory()

    def receive_info(self, info):
        if "story" in info:
            story = info["story"]
            print(f"**PlayerAgent**: 题目：{story}")
            self.messages.append({"role": "user", "content": "题目：" + story})
        elif "user_known_info" in info:
            user_known_info = info["user_known_info"]
            print(f"**PlayerAgent**: 已掌握的信息：{user_known_info}")
            self.messages.append({"role": "user", "content": "已掌握的信息：" + user_known_info})
        if len(self.messages) >= 20:
            self.messages.pop(2)

    def answer(self):
        try:
            if not self.messages:
                return
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            answer = response.choices[0].message.content
            print(f"**Player Agent**: {answer}")
            return answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

