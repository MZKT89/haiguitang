class Memory:
    def __init__(self):
        self.story = None
        self.truth = None
        self.user_known_info = []

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
        return self.user_known_info
    
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