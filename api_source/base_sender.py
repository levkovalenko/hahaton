import requests
import json
import datetime


main_fields = ['BU', 'ETU', 'ETB', 'EOU', 'EOB']


class SendError(Exception):
    def __init__(self, *args, **kwargs):

        # Call the base class constructor with the parameters it needs
        super().__init__(*args, **kwargs)


class DataSender:
    def __init__(self, url='http://127.0.0.1:8000/portf/'):
        self.url = url

    def send_data(self, name: str, data: dict):
        """
        Function for sending data to url.
        :param name: type of data
        :param data: data for sending
        """
        loc_data = dict()
        for field in main_fields:
            if field in data:
                loc_data[field] = data[field]

        loc_data['type'] = name
        loc_data['time'] = str(datetime.datetime.now())

        t = requests.post(self.url, json=json.dumps(loc_data))

        if t.status_code != 200:
            raise SendError('sendError')

    def send_bucket(self, data: dict):
        """
        Function for sending bucket status
        :param data: current bucket information
        """
        self.send_data("bucket", data)

    def send_price(self, data: dict):
        """
        Function for sending price status
        :param data: current price information
        """
        self.send_data("price", data)

    def send_volatility(self, data: dict):
        """
        Function for sending volatility status
        :param data: current volatility information
        """
        self.send_data("vol", data)


if __name__ == '__main__':
    s = DataSender()
    s.send_bucket({"BU": 7})
