from vkbottle import Bot, load_blueprints_from_package
import config
from loguru import logger
import os
from typing import Optional

import lottery
# logger.disable("vkbottle")

class WinBot(Bot):
    def __init__(self, token):
        super().__init__(token)
        self.lottery: lottery.Lottery = Optional

bot = WinBot(os.environ["KEY"])

for bp in load_blueprints_from_package("blueprints"):
    bp.load(bot)

bot.run_forever()
