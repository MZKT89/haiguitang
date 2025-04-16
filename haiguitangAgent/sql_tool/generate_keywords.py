import openai
import sqlite3
from ..config.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
from tqdm import tqdm 

def summarize_keywords(story):
    """
    使用 LLM 总结故事的关键词
    """
    prompt = f"请根据以下海龟汤故事内容总结出关键词，关键词之间用逗号分隔：\n{story}，只输出关键词，不需要其他内容，关键词不需要包含海龟汤这三个字，与内容相关即可。"
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    models = client.models.list()
    print("models:", models)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "你是一个擅长总结关键词的助手。"},
            {"role": "user", "content": prompt}
        ]
    )
    print("response:", response)
    keywords = response.choices[0].message.content.strip()
    return keywords


def update_keywords_in_database():
    """
    从数据库中获取所有记录，并使用 LLM 更新关键词
    """
    conn = sqlite3.connect('haiguitangAgent/sql_tool/turtle_soup.db')
    cursor = conn.cursor()

    try:
        # 查询所有记录
        query = "SELECT id, story FROM turtle_soup_stories"
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in tqdm(results, desc="更新关键词进度", unit="条"):
            story_id, story = row
            keywords = summarize_keywords(story)
            print(f"keywords: {keywords}")
            # 更新数据库中的关键词
            update_query = "UPDATE turtle_soup_stories SET keywords =? WHERE id =?"
            cursor.execute(update_query, (keywords, story_id))

        # 提交事务
        conn.commit()
        print("已成功更新数据库中的所有关键词。")
    except Exception as e:
        print(f"更新关键词时出现错误: {e}")
        conn.rollback()
    finally:
        # 关闭数据库连接
        conn.close()


# 调用函数更新数据库中的关键词
# update_keywords_in_database()

print(summarize_keywords("我终于放学了"))