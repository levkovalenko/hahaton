import requests
import json
import datetime
import socket
import abc


main_fields = ['BU', 'ETU', 'ETB', 'EOU', 'EOB']


class SendError(Exception):
    def __init__(self, *args, **kwargs):

        # Call the base class constructor with the parameters it needs
        super().__init__(*args, **kwargs)


class BaseSender(abc.ABC):

    @abc.abstractmethod
    def send_data(self, name: str, data: dict, time=None):
        pass

    def dump_data(self, name: str, data: dict, time=None) -> str:
        """
        function for creating sending dict
        :param name: type of data
        :param data: data for sending
        :param time: time for sending
        :return: bode of sending request
        """
        loc_data = dict()
        for field in main_fields:
            if field in data:
                loc_data[field] = data[field]

        loc_data['type'] = name
        if time is None:
            time = datetime.datetime.now()
        loc_data['time'] = str(time)
        return json.dumps(loc_data)

    def send_bucket(self, data: dict, time=None):
        """
        Function for sending bucket status
        :param data: current bucket information
        :param time: time for sending
        """
        self.send_data("bucket", data, time=time)

    def send_price(self, data: dict, time=None):
        """
        Function for sending price status
        :param data: current price information
        :param time: time for sending
        """
        self.send_data("price", data, time=time)

    def send_volatility(self, data: dict, time=None):
        """
        Function for sending volatility status
        :param data: current volatility information
        :param time: time for sending
        """
        self.send_data("vol", data, time=time)


class TCPSender(BaseSender):
    def __init__(self, ip='localhost', port=9090):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.connect()

    def send_data(self, name: str, data: dict, time=None):
        """
        Function for sending data to tcp.
        :param name: type of data
        :param data: data for sending
        :param time: time for sending
        """
        str_data = self.dump_data(name, data, time)

        self.socket.send(str_data.encode())

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def drop_connection(self):
        self.socket.close()


class HTTPSender(BaseSender):

    def __init__(self, url='http://127.0.0.1:8000/portf/'):
        self.url = url

    def send_data(self, name: str, data: dict, time=None):
        """
        Function for sending data to url.
        :param name: type of data
        :param data: data for sending
        :param time: time for sending
        """
        str_data = self.dump_data(name, data, time)

        t = requests.post(self.url, json=str_data)

        if t.status_code != 200:
            raise SendError('sendError')


if __name__ == '__main__':
    s = HTTPSender()
    s.send_bucket({"BU": 7})
