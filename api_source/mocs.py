import api_source.moc_bucket as moc
import api_source.base_sender as sender
import api_source.moc_volatility as pv
import time
import datetime


def http_bucket(period=10, moc_period=datetime.timedelta(seconds=5), url=None):
    buc = moc.Bucket(period=moc_period)
    if url is None:
        s = sender.HTTPSender()
    else:
        s = sender.HTTPSender(url=url)
    while True:
        buc.update()
        s.send_bucket(buc.val)
        print(buc.val)
        time.sleep(period)


def tcp_bucket(period=10, moc_period=datetime.timedelta(seconds=5), ip='localhost', port=9090):
    buc = moc.Bucket(period=moc_period)
    s = sender.TCPSender(ip=ip, port=port)
    while True:
        buc.update()
        s.send_bucket(buc.val)
        print(buc.val)
        time.sleep(period)


def tcp_pv(period=10, moc_period=datetime.timedelta(seconds=5), ip='localhost', port=9090):
    buc = pv.VolatilityPrice(period=moc_period)
    s = sender.TCPSender(ip=ip, port=port)
    while True:
        buc.update()
        s.send_price(buc.price)
        print(buc.price)
        s.send_volatility(buc.vol)
        print(buc.vol)
        time.sleep(period)
