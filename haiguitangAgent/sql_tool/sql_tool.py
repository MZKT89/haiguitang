from dotenv import load_dotenv
import os
import json
import sqlite3
from haiguitangAgent.config.config import DB_PATH
# 示例的 SQL 查询参数
sql_inter_args = '{"keyword": "恐怖", "create_new_story": false}'

# 定义 sql_inter 工具的元信息
sql_inter_tool = {
    "type": "function",
    "function": {
        "name": "sql_inter",
        "description": (
            "该工具用于与海龟汤游戏的 SQLite 数据库进行交互。主要功能包括："
            "1. 根据关键词从数据库中搜索海龟汤故事，从搜索结果中选择一个故事，并将其 ID 记录到缓存列表中，以标记该故事已被玩过。"
            "2. 如果从数据库中获取的海龟汤故事不够精彩，可自主出题并将新故事按照规定格式添加到数据库中。"
            "使用时，请确保传入的参数为符合 JSON 格式的字符串，例如："
            f"{sql_inter_args}"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "用于搜索海龟汤故事的关键词。"
                },
                "create_new_story": {
                    "type": "boolean",
                    "description": "是否自主出题添加新的海龟汤故事到数据库，默认为 False。",
                    "default": False
                },
                "story_content": {
                    "type": "string",
                    "description": "当 create_new_story 为 True 时，提供新海龟汤故事的内容。"
                },
                "keywords": {
                    "type": "string",
                    "description": "当 create_new_story 为 True 时，提供新海龟汤故事的关键词，多个关键词用逗号分隔。"
                },
                "g": {
                    "type": "string",
                    "description": "全局环境变量，默认值为 globals()。",
                    "default": "globals()"
                }
            },
            "required": []
        }
    }
}

# 初始化缓存字典和已使用 ID 列表
cache = {}
used_ids = []

def sql_inter(keyword=None, create_new_story=False, story_content=None, keywords=None, g='globals()'):
    """
    该函数用于与海龟汤游戏的 SQLite 数据库进行交互。具体功能如下：
    1. 如果传入 keyword 参数，会根据关键词从数据库中搜索海龟汤故事，选择一个故事并将其 ID 记录到缓存列表中。
    2. 如果 create_new_story 为 True，会自主出题并将新故事添加到数据库中。

    :param keyword: 用于搜索海龟汤故事的关键词。
    :param create_new_story: 是否自主出题添加新的海龟汤故事到数据库，默认为 False。
    :param story_content: 当 create_new_story 为 True 时，提供新海龟汤故事的内容。
    :param keywords: 当 create_new_story 为 True 时，提供新海龟汤故事的关键词，多个关键词用逗号分隔。
    :param g: 全局环境变量，默认值为 globals()。
    :return: 执行操作的结果或反馈信息。
    """
    print("正在调用 sql_inter 工具执行数据库操作...")
    # 获取 SQLite 数据库文件路径
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()
        if keyword:
            if keyword in cache:
                # 缓存命中，从缓存中获取未使用过的故事 ID
                available_ids = [id for id in cache[keyword] if id not in used_ids]
                if available_ids:
                    story_id = available_ids[0]
                    # 执行查询获取故事详情
                    cursor.execute("SELECT id, story, keywords FROM turtle_soup_stories WHERE id =?", (story_id,))
                    selected_story = cursor.fetchone()
                    # 将故事 ID 添加到已使用 ID 列表
                    used_ids.append(story_id)
                    print(f"已选择故事 ID 为 {story_id} 的海龟汤故事，并记录到已使用 ID 列表中。")
                    return json.dumps(selected_story)
                else:
                    print(f"缓存中没有包含关键词 '{keyword}' 且未使用过的海龟汤故事，重新查询数据库。")
            
            # 根据关键词搜索海龟汤故事，排除已玩过的故事
            search_query = f"SELECT id, story, keywords FROM turtle_soup_stories WHERE keywords LIKE '%{keyword}%'"         
            cursor.execute(search_query)
            results = cursor.fetchall()
            if results:
                # 存储查询结果到缓存
                cache[keyword] = [row[0] for row in results]
                # 选择一个故事
                selected_story = results[0]
                story_id = selected_story[0]
                # 将故事 ID 添加到已使用 ID 列表
                used_ids.append(story_id)
                print(f"已选择故事 ID 为 {story_id} 的海龟汤故事，并记录到已使用 ID 列表中。")
                return json.dumps(selected_story)
            else:
                print(f"未找到包含关键词 '{keyword}' 的海龟汤故事。")
                return json.dumps([])
        elif create_new_story:
            if not story_content or not keywords:
                print("当 create_new_story 为 True 时，必须提供 story_content 和 keywords。")
                return json.dumps({"error": "缺少必要参数"})
            # 插入新的海龟汤故事到数据库
            insert_query = "INSERT INTO turtle_soup_stories (story, keywords) VALUES (?, ?)"
            cursor.execute(insert_query, (story_content, keywords))
            connection.commit()
            new_story_id = cursor.lastrowid
            used_ids.append(new_story_id)
            print(f"已成功添加新的海龟汤故事，ID 为 {new_story_id}。记录到已使用 ID 列表中。")
            return json.dumps({"new_story_id": new_story_id})
        else:
            print("未提供有效的参数，请检查输入。")
            return json.dumps({"error": "未提供有效参数"})
    except Exception as e:
        print(f"执行数据库操作时出现错误: {e}")
        return json.dumps({"error": str(e)})
    finally:
        connection.close()
