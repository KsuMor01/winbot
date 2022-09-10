import typing
from typing import Optional
import time
import datetime

class Lottery:
    def __init__(self, word, post, num, start_time: Optional = None, end_time: Optional = None, duration: Optional = datetime.datetime.day):
        self.win_word = word
        self.wall_post = post
        self.num_of_winners = num
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.in_process = False

        self.participants = []

    @property
    def lottery_status(self):
        return {
            'in_process': self.in_process,
            'wall_post': self.wall_post,
            'win_word': self.win_word
        }

    def start_lottery(self):
        pass

    def stop_lottery(self):
        pass
