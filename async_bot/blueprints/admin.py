import os

from vkbottle.bot import Blueprint, Message, rules, MessageEvent
from vkbottle_types.objects import MessagesConversation
from vkbottle.dispatch.rules import ABCRule
from vkbottle.api import API

from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, ShowSnackbarEvent

from typing import Optional

from lottery import Lottery


class GroupAdmins(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        res = await api.request("groups.getMembers", {"group_id": event.group_id, "filter": "manager"})
        admins = res['response']['items']
        return event.from_id in admins


bp = Blueprint("for admin commands")
bp.labeler.vbml_ignore_case = True

api = API(os.environ["KEY"])

bp.labeler.auto_rules = [GroupAdmins()]


LOTTERY_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Callback("Розыгрыш", payload={"cmd": "lottery_status"}))
    .get_json()
)
NEW_LOTTERY = (
    Keyboard(one_time=True)
    .add(Callback("Создать новый розыгрыш", payload={"cmd": "new_lottery"}))
    .get_json()
)

cur_lottery = Optional


@bp.on.private_message(command='start')
async def start_lottery(message: Message):
    await message.answer("Начнем! Нажми на кнопку, чтобы узнать о статусе розыгрыша", keyboard=LOTTERY_KEYBOARD)


@bp.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadContainsRule({"cmd": "lottery_status"}),
)
async def lottery_status(event: MessageEvent):
    try:
        # cur_lottery = Lottery(word='win', post="smth", num=2)
        await event.send_message(message=cur_lottery.lottery_status)
    except AttributeError:
        await event.send_message(message='no lottery is configured!')



@bp.on.private_message(command='stop')
async def stop_lottery(message: Message):
    await message.answer("stop lottery")
