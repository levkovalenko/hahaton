import api_source.mocs as moc
import datetime


if __name__ == '__main__':
    dt = datetime.timedelta(seconds=4)
    moc.tcp_bucket(period=4, moc_period=dt, ip='172.20.197.19')
    #moc.tcp_pv(period=10, moc_period=dt)
