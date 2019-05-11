import api_source.base_sender as sender
import datetime
import random


class VolatilityPrice:
    def __init__(self, period=datetime.timedelta(seconds=1)):
        print(period)
        self.vol = dict()
        self.price = dict()
        for field in sender.main_fields:
            self.vol[field] = 0
            self.price[field] = 0
        self.last_update = datetime.datetime.now()
        self.period = period

    def update(self):
        if datetime.datetime.now() > self.last_update + self.period:
            self.last_update = datetime.datetime.now()
            for key in self.vol.keys():
                t = random.uniform(-1, 1)
                self.price[key] = self.price[key] + t
                self.vol[key] = self.vol[key] + t * random.uniform(0.9, 1.1)
