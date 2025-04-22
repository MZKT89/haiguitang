class Memory:
    def __init__(self):
        self.story = None
        self.truth = None
        self.user_known_info = []
        self.left_question_chance = None
        self.left_answer_chance = None

    def store_story_and_truth(self, story, truth):
        self.story = story
        self.truth = truth

    def add_user_known_info(self, info):
        self.user_known_info.append(info)

    def get_story(self):
        return self.story

    def get_truth(self):
        return self.truth

    def get_user_known_info(self):
        info_str = ""
        info_len = len(self.user_known_info)
        for i, info in enumerate(self.user_known_info):
            current_info = str(i+1) + ". " + info
            info_str += current_info
            if i + 1 < info_len:
                info_str += "\n"
        return info_str
    
    def set_left_question_chance(self, value):
        self.left_question_chance = value

    def set_left_answer_chance(self, value):
        self.left_answer_chance = value
    
    def to_player_agent(self):
        msgs = {}
        if self.story:
            msgs["story"] = self.story
        if self.user_known_info:
            msgs["user_known_info"] = "; ".join(self.user_known_info)
        if self.left_question_chance is not None:
            msgs["left_question_chance"] = str(self.left_question_chance)
        if self.left_answer_chance is not None:
            msgs["left_answer_chance"] = str(self.left_answer_chance)
        return msgs
    
    def to_messages(self):
        content_parts = []
        if self.story:
            content_parts.append(f"当前海龟汤游戏的故事情节: {self.story}")
        if self.truth:
            content_parts.append(f"当前海龟汤游戏的故事真相: {self.truth}")
        if self.user_known_info:
            content_parts.append("用户已掌握的信息如下:")
            for info in self.user_known_info:
                content_parts.append(info)

        combined_content = "\n".join(content_parts)
        if combined_content:
            return [{"role": "system", "content": combined_content}]
        return []
    
    def reset(self):
        self.story = None
        self.truth = None
        self.user_known_info = []