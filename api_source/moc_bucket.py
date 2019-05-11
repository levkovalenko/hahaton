import api_source.base_sender as sender
import datetime
import random


class Bucket:
    def __init__(self, period=datetime.timedelta(minutes=10)):
        print(period)
        self.val = dict()
        for field in sender.main_fields:
            self.val[field] = 0
        self.val['sum'] = 0
        self.last_update = datetime.datetime.now()
        self.period = period

    def update(self):
        if datetime.datetime.now() > self.last_update + self.period:
            self.last_update = datetime.datetime.now()
            for key in self.val.keys():
                t = random.uniform(-1, 1)
                self.val[key] = self.val[key] + t
                self.val['sum'] = self.val['sum'] + t*random.uniform(0.9, 1.1)

