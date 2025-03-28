import os
import random
import yaml
from astrbot.api.all import *

PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_answerbook')
ANSWER_BOOK_FILE = os.path.join(PLUGIN_DIR, 'answer_book.yml')

@register("answer_book", "浅夏旧入梦", "一个简单的答案之书插件", "1.0.0")
class AnswerBookPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.answer_book = self._load_answer_book()
    def _load_answer_book(self):
        """加载答案书"""
        try:
            with open(ANSWER_BOOK_FILE, 'r', encoding='gbk') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.context.logger.error(f"加载答案之书文本库失败: {str(e)}")
            return {}
            
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群聊消息处理器"""
        msg = event.message_str.strip()
        msg_id = str(event.message_obj.message_id)
        if msg.startswith("答案之书"):
        # 随机选择一个答案
            answer = random.choice(self.answer_book)
            answer_text=str(answer)
            chain = [
                Reply(id=msg_id),
                Plain(text=answer_text)
            ]
            yield event.chain_result(chain)
