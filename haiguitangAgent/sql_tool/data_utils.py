import json
import sqlite3

# 定义 JSON 文件路径和数据库文件路径
json_file_path = 'turtle.json'
db_file_path = 'turtle_soup.db'


def create_database_from_json(json_file_path, db_file_path):

    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    # 创建表
    create_table_query = """
    CREATE TABLE IF NOT EXISTS turtle_soup_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keywords TEXT NOT NULL,
        story TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)

    # 读取 JSON 文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 插入数据到数据库表
        for item in data:
            # 去掉关键词前的 “关键词：” 字样
            keywords = item['input'].replace("关键词：", "")
            story = item['output']
            insert_query = "INSERT INTO turtle_soup_stories (keywords, story) VALUES (?,?)"
            cursor.execute(insert_query, (keywords, story))

        # 提交事务
        conn.commit()
        print("数据已成功插入数据库。")
    except FileNotFoundError:
        print(f"未找到 JSON 文件: {json_file_path}")
    except json.JSONDecodeError:
        print(f"JSON 文件解析出错: {json_file_path}")
    except Exception as e:
        print(f"插入数据时出现错误: {e}")
        conn.rollback()
    finally:
        # 关闭数据库连接
        conn.close()


def deduplicate_stories():
    """
    对 turtle_soup_stories 表中的故事根据 story 字段进行去重
    """
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    try:
        # 查询所有故事及其出现次数
        query_count = "SELECT story, COUNT(*) as count FROM turtle_soup_stories GROUP BY story HAVING COUNT(*) > 1"
        cursor.execute(query_count)
        duplicate_stories = cursor.fetchall()

        for story, count in duplicate_stories:
            # 查询重复故事的所有记录的 ID
            query_ids = "SELECT id FROM turtle_soup_stories WHERE story =?"
            cursor.execute(query_ids, (story,))
            story_ids = cursor.fetchall()

            # 删除除第一条外的其他重复记录
            for i in range(1, len(story_ids)):
                delete_query = "DELETE FROM turtle_soup_stories WHERE id =?"
                cursor.execute(delete_query, (story_ids[i][0],))
                print(f"已删除 ID 为 {story_ids[i][0]} 的重复故事记录")

        # 提交事务
        conn.commit()
        print("已成功对数据库中的故事进行去重。")
    except Exception as e:
        print(f"去重时出现错误: {e}")
        conn.rollback()
    finally:
        # 关闭数据库连接
        conn.close()

deduplicate_stories()