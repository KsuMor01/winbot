import os

from vkbottle.bot import Blueprint, Message, rules, MessageEvent
from vkbottle_types.objects import MessagesConversation
from vkbottle.dispatch.rules import ABCRule
from vkbottle.api import API

from vkbottle import Callback, GroupEventType, Text, Keyboard, BaseStateGroup, EMPTY_KEYBOARD

from typing import Optional

from lottery import Lottery


class MenuState(BaseStateGroup):
    STATUS = 0
    NEW = 1
    WORD = 2
    POST = 3



class GroupAdmins(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        api = API(os.environ["KEY"])
        res = await api.request("groups.getMembers", {"group_id": event.group_id, "filter": "manager"})
        admins = res['response']['items']
        return event.from_id in admins


bp = Blueprint("for admin commands")
bp.labeler.vbml_ignore_case = True
bp.labeler.auto_rules = [GroupAdmins()]

cur_lottery = Optional


@bp.on.private_message(state=None)
async def start_lottery(message: Message):
    keyboard = (
        Keyboard()
        .add(Text("Розыгрыш", payload={"cmd": "lottery_status"}))
        .get_json()
    )
    await message.answer("Нажми на кнопку, чтобы узнать о статусе розыгрыша", keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, MenuState.STATUS)


@bp.on.private_message(state=MenuState.STATUS, payload={"cmd": "lottery_status"})
async def lottery_status(message: Message):
    keyboard = (
        Keyboard()
        .add(Text("Создать", payload={"cmd": "new_lottery"}))
        .get_json()
    )

    try:
        # cur_lottery = Lottery(word='win', post="smth", num=2)
        await message.answer(message=cur_lottery.lottery_status)
    except AttributeError:
        await message.answer(message="Ни одного розыгрыша не создано! Создать новый?", keyboard=keyboard)
        await bp.state_dispenser.set(message.peer_id, MenuState.NEW)


@bp.on.private_message(state=MenuState.NEW, payload={"cmd": "new_lottery"})
async def new_lottery(message: Message):
    keyboard = (
        Keyboard()
        .add(Text("Пост розыгрыша", payload={"cmd": "wall_post"}))
        .add(Text("Слово для участия", payload={"cmd": "word"}))
        .add(Text("Время проведения", payload={"cmd": "time"}))
        .get_json()
    )

    await message.answer(message="Создание нового розыгрыша.", keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, MenuState.POST)

@bp.on.private_message(state=MenuState.POST, payload={"cmd": "wall_post"})
async def wall_post(message: Message):
    print(await bp.state_dispenser.get(message.peer_id))
    await message.answer(message="Вставьте ссылку на пост с розыгрышем.", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, MenuState.NEW)

