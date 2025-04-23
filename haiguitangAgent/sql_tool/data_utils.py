import json
import sqlite3

# 定义 JSON 文件路径和数据库文件路径
json_file_path = 'turtle.json'
# db_file_path = 'turtle_soup.db'
db_file_path = './haiguitangAgent/sql_tool/turtle_soup.db'

import sqlite3

def get_qids():
    print("[DEBUG] db_file_path {db_file_patch}")
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    qids = []
    try:
        # 执行 SQL 查询，从 turtle_soup_stories 表中选择所有的 id
        cursor.execute("SELECT id FROM turtle_soup_stories")
        # 获取所有查询结果
        results = cursor.fetchall()
        # 遍历结果，将每个 id 添加到 qids 列表中
        for row in results:
            qids.append(row[0])
    except sqlite3.Error as e:
        print(f"Error occurred while querying the database: {e}")
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()
    return qids

def update_fisrt_few_story():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    # 更新前 10 条记录的 story 字段 
    update_query = "UPDATE turtle_soup_stories SET story = ? WHERE id = ?"
    my_story = [
        {
            "keywords": "盲人，生日，朋友",   
            "story": "故事情节：曾经有一个盲人，他过生日时候，他的同生共死过的好伙伴们来一起为他庆生，他开心的吹完蜡烛唱完生日歌后，大家为其鼓掌和祝福，听到掌声的盲人把他们都杀了。真相：男主和朋友曾经一起去探险，一段时间后没有了食物，因为男主本身是一个盲人，所以这帮朋友都骗他说每人砍下一只手来吃，可最后只砍了男主一个人的手。之后有一次男主邀请朋友们来参加自己的生日聚会，吹完蜡烛后所有人都鼓掌了，男主发现只有自己的手被砍下来吃了，男主无法忍受这样的欺骗于是杀了所有的好朋友。"
        },
        {
            "keywords": "男孩，餐厅",       
            "story": "故事情节：一个男孩儿走进一家餐厅，喝了一碗海龟汤，然后他就自杀了。真相：这个男孩儿跟爸爸一起出海，中途遇到暴风，在弥留之际，爸爸用自己的肉给他熬了一碗汤，骗他的儿子说这是海龟熬成的汤，爸爸牺牲自己保住了孩子的性命。孩子安全上岸之后，去了餐厅点了一碗真正的海龟汤，发现原来不是那个味道，顿时明白了，就自杀了。"
        },
        {
            "keywords": "三兄弟，睡觉", 
            "story": "故事情节：以前有三兄弟，大哥和二哥是双胞胎，三兄弟关系非常好，常常一起睡觉，大哥病死后，三弟把二哥杀了，为什么。真相：三弟有神经病，大哥病死后，弟弟把二哥分尸成左右两半，左边睡二哥的右半边身，右边睡二哥的左半边身，这样看起来大哥就好像没死一样"
        },
        {
            "keywords": "妈妈，捉迷藏", 
            "story": "故事情节：我跟妈妈玩捉迷藏，当妈妈看到我时，我却一动也不能动了。真相：我跟妈妈在家玩捉迷藏，我藏到了床底下，随着咚咚咚的脚步声，我知道妈妈要进来了，可当门被打开后，我看到了妈妈的眼睛，她倒在地上，身体被人拖着，我捂着口鼻一动也不敢动。"
        },
        {
            "keywords": "儿子，妻子", 
            "story": "故事情节：我的儿子非常崇拜我，有一天回到家，妻子死了，儿子对我说了一句话，我疯了。真相：爸爸是魔术师，儿子为了效仿爸爸的大变活人，把妈妈切开了，对爸爸说现在轮到你把她变回去了。"
        },
        {
            "keywords": "损坏", 
            "story": "故事情节：一个人损坏了另一个人刚刚买的东西，然而后者什么都没说就走了，请问发生了什么？真相：电影院检票"
        },
        {
            "keywords": "出租车", 
            "story": "故事情节：一个人从一间屋子里出来，伸手招了辆出租车，然后他再也没能回来这间屋子，请问这是为什么？真相：这个人是小偷，出租车司机是这间屋子的主人，于是直接带着他开去了警察局。"
        },
        {
            "keywords": "让座", 
            "story": "故事情节：一天，小明和老明一同乘公交车。老明是一名年近八旬的老人，小明则是一名年轻的小伙子。上车后，乘客却纷纷给小明让座，这是为什么？真相：小明挤上了车后发现无人给老人让座，于是大吼一声:“快给大爷让个座!”几个胆小的乘客看见小明一脸凶相，以为“大爷”指的是小明自己，于是起身给他让座。"
        },
        {
            "keywords": "裤子", 
            "story": "故事情节：我的裤子破了，我知道我马上要死了。真相：我是一名宇航员，这一天我正身着宇航服在太空中执行任务，突然我发现我的裤子破了，之后我暴露在没有气压和氧气的太空中，不到几秒钟，我将死去。"
        },
        {
            "keywords": "电梯", 
            "story": "故事情节：一个人住在20层。每天早上，他会做电梯下到1楼。每天晚上他会坐到16楼，然后走楼梯回家，除非当天下雨或者有人同乘电梯。请问这是为什么？真相：这个人很矮，够不到20楼的按钮。除非用雨伞或者有别人帮他。"
        }
    ]
    for i, story_info in enumerate(my_story, start = 1):
        story = story_info["story"]
        cursor.execute("UPDATE turtle_soup_stories SET story = ?, keywords = ? WHERE id = ?", 
                       (story, story_info["keywords"], i))
    conn.commit()
    conn.close()

def add_new_soup():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    my_story = [
        {
            "keywords": "高楼，电梯",
            "story": "故事情节：一个人离他的车有好几十米，但是他只走了几步就上车了，这是为什么？真相：他在高楼上班，坐电梯到地下车库上车，他的车停得离电梯口很近，几步就走到了。"
        },
        {
            "keywords": "夫妇，密室，神秘人",
            "story": "故事情节：有一对夫妇，丈夫深夜开车带妻子在路上，很快车就没油了，丈夫锁上门去附近的加油站取，回来发现车完好无损，但车里多了一个人。请问，这是为什么？真相：妻子快生了，丈夫开车去医院。取油回来发现妻子已经在车里生了，所以就多了一个人。"
        },
        {
            "keywords": "生日，鼓掌，断手",
            "story": "故事情节：一个人过生日，邀请他所有的好朋友来参加。吹完蜡烛的时候，这个人把他所有的好朋友都杀了，为什么？真相：男主和朋友曾经一起去探险，一段时间后没有了食物，因为男主本身是一个盲人，所以这帮朋友都骗他说每人砍下一只手来吃，可最后只砍了男主一个人的手。之后有一次男主邀请朋友们来参加自己的生日聚会，吹完蜡烛后所有人都鼓掌了，男主发现只有自己的手被砍下来吃了，男主无法忍受这样的欺骗于是杀了所有的好朋友。"
        },
        {
            "keywords": "空屋子，画像，窗户",
            "story": "故事情节：深夜，迷路的女孩找到了间空屋子，墙上挂了一幅画像，她很疲惫但她睡不着。第二天清晨，累得睡着的她醒过来，发现了异样，恐惧地逃离了屋子。真相：女孩睡觉的时候，觉得画像里的人在盯着她看，内心不安无法入睡。第二天早上女孩醒来发现画像里的人不见了，意识到墙上的不是画，而是窗户，昨晚窗外有人盯着她看，发觉了真相的女孩吓坏了，逃离了屋子。"
        },
        {
            "keywords": "小偷，出租车",
            "story": "故事情节：一个人从一间屋子里出来，伸手招了辆出租车，然后他再也没能回来这间屋子，请问这是为什么？真相：这个人是小偷，出租车司机是这间屋子的主人，于是直接带着他开去了警察局。"
        },
        {
            "keywords": "镜子，时钟，吃药",
            "story": "故事情节：我从梦中醒来，看了一眼镜子中的时钟，继续躺下，但是却永远地睡了过去，为什么？真相：我患有某种致命的疾病，必须每隔一段时间就吃药。我从梦中醒来，查看现在是否是我需要吃药的时间。但是这次迷迷糊糊中，我忘记了镜子中的时间是相反的，我以为离自己吃药还有很长的时间，就又睡了过去，最终我因为没有及时吃药而病发身亡。"
        },
    ]
    insert_query = "INSERT INTO turtle_soup_stories (keywords, story) VALUES (?,?)"
    for story_info in my_story:
        keywords = story_info["keywords"]
        story = story_info["story"]
        cursor.execute(insert_query, (keywords, story))
    conn.commit()
    conn.close()

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

# deduplicate_stories()
def read_story_by_id(story_id):
    """
    根据故事 ID 从数据库中读取故事
    :param story_id: 故事 ID
    :return: 故事内容
    """
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    try:
        query = "SELECT story FROM turtle_soup_stories WHERE id = ?"
        cursor.execute(query, (story_id,))
        result = cursor.fetchone()
        if result:
            full_story = result[0]
            # 假设故事情节和真相之间有固定的分隔符 "真相："
            parts = full_story.split("真相：")
            if len(parts) == 2:
                story = parts[0].replace("故事情节：", "").strip()
                truth = parts[1].strip()
                return story, truth
            else:
                print(f"无法正确解析 ID 为 {story_id} 的故事。")
                return None
        else:
            print(f"未找到 ID 为 {story_id} 的故事。")
            return None
    except Exception as e:
        print(f"查询故事时出现错误: {e}")
        return None
    finally:
        conn.close()

# story, truth = read_story_by_id(1)
# print("故事情节:", story)
# print("故事真相:", truth)
# add_new_soup()

# update_fisrt_few_story()