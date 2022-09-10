import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.utils import get_random_id
import random
import config
import winbot
import lottery
import message_handler


bot = winbot.WinBot(token=config.KEY, group_id=config.GROUP_ID)

bot.start_listener()


for event in bot.listener:
    print(event.type)

    if event.type == VkBotEventType.MESSAGE_NEW:
        print(event.raw)

        if bot.user_is_admin(event.message.from_id):
            message_text = event.message.text
            user_id = event.message.from_id

            if bot.is_command(message_text):

                if message_text == "розыгрыш":
                    bot.lottery = lottery.Lottery(word='win', num=1, post=1)
                    try:
                        # print(bot.lottery.lottery_status)
                        bot.send_message(user_id, bot.lottery.lottery_status["in_process"])
                    except AttributeError:
                        bot.create_new_lottery(user_id)

                if message_text == "начать":
                    continue

# comments listener
#
# longpoll = VkBotLongPoll(vk_session, config.GROUP_ID)
# vk = vk_session.get_api()
# print(vk_session.scope)
#
# participants = []
#
# for event in longpoll.listen():
#     print(event.raw['object']['text'] == win_word)
#     if event.type == VkBotEventType.WALL_REPLY_NEW and event.raw['object']['text'] == win_word:
#         print(event.raw)
#         participants.append(event.raw['object']['id'])
#         print(participants)
#
#     # after the end of lottery
#         for winner in random.sample(participants, num_of_winners):
#             print(winner)
#
#             vk.wall.createComment(reply_to_comment=winner, access_token=config.KEY,
#                                   owner_id=event.raw['object']['owner_id'], from_group=event.raw['group_id'],
#                                   post_id=event.raw['object']['post_id'], message='YOU WON')
#

