import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from typing import Optional
from vk_api.utils import get_random_id

import lottery
import message_handler


class WinBot:
    def __init__(self, token, group_id):
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()
        self.group_id = group_id
        self.longpoll = VkBotLongPoll(self.session, group_id)
        self.commands = ["розыгрыш", "закончить"]
        self.lottery = Optional
        self.listener = Optional

    def start_listener(self):
        self.listener = self.longpoll.listen()

    def stop_listener(self):
        pass

    def send_message(self, user_id, text):
        self.vk.messages.send(
            message=text,
            random_id=get_random_id(),
            peer_id=user_id
        )

    def create_new_lottery(self, user_id):
        self.send_message(user_id, 'No lottery is configured!')

    def get_admins(self):
        for user in self.vk.groups.getMembers(group_id=self.group_id, filter='managers')['items']:
            yield user['id']

    def user_is_admin(self, user_id):
        if user_id in [admin for admin in self.get_admins()]:
            return True
        else:
            return False

    def is_command(self, text):
        if text in self.commands:
            return True
        else:
            return False



