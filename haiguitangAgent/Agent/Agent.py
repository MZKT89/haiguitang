import os
from dotenv import load_dotenv
import openai
from IPython.display import display, Markdown
import json
from haiguitangAgent.sql_tool.sql_tool import sql_inter, sql_inter_tool
from haiguitangAgent.config.config import DS_API_KEY, DS_BASE_URL, DS_MODEL, OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
from haiguitangAgent.Agent.prompt import agent_prompt
from rich.console import Console
from haiguitangAgent.Memory.Memory import Memory


class TurtleSoupAgent:
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

        if messages is not None:
            self.messages = messages
        else:
            self.messages = [{"role": "system", "content": agent_prompt}] + self.memory.to_messages()

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        print(f"client: {self.client}")

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
                response_data = json.loads(content)
                should_reset = response_data.get("new_game", False)
                if should_reset:
                    self.memory.reset()
                    print("记忆已重置，开始新游戏。")
                if "story" in response_data and "truth" in response_data:
                    self.memory.store_story_and_truth(response_data["story"], response_data["truth"])
                    # 更新messagelist的memory
                    # self.messages[1] = self.memory.to_messages()[0]
                    self.messages[1:2] = self.memory.to_messages()
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


tools = [sql_inter_tool]
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
            tools=tools,
            response_format={
                'type': 'json_object'
            }
        )        
    except Exception as e:
        print("模型调用报错" + str(e))
        return None

    if response.choices[0].finish_reason == "tool_calls":
        print("[Debug]模型响应中包含外部函数调用请求，正在处理...")
        print(response)
        print("=============================================")
        while True:
            messages = create_function_response_messages(messages, response)
            response = client.chat.completions.create(
                model=model,  
                messages=messages,
                tools=tools,
            )

            if response.choices[0].finish_reason != "tool_calls":
                break
    return response

def create_function_response_messages(messages, response):
    
    """
    调用外部工具，并更新消息列表
    :param messages: 原始消息列表
    :param response: 模型某次包含外部工具调用请求的响应结果
    :return：messages，追加了外部工具运行结果后的消息列表
    """

    available_functions = {
        "sql_inter": sql_inter,
    }
    
    # 提取function call messages
    function_call_messages = response.choices[0].message.tool_calls

    # 将function call messages追加到消息列表中
    messages.append(response.choices[0].message.model_dump())

    for function_call_message in function_call_messages:
        tool_name = function_call_message.function.name
        tool_args = json.loads(function_call_message.function.arguments)       
        fuction_to_call = available_functions[tool_name]
        try:
            tool_args['g'] = globals()
            # 运行调用的tool
            function_response = fuction_to_call(**tool_args)
        except Exception as e:
            function_response = "函数运行报错如下:" + str(e)

        # 拼接消息队列
        messages.append(
            {
                "role": "tool",
                "content": function_response,
                "tool_call_id": function_call_message.id,
            }
        )
        
    return messages     


if __name__ == "__main__":
    assistant = TurtleSoupAgent()
    assistant.chat("我想玩一个校园相关海龟汤")

