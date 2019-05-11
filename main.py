import api_source.mocs as moc
import datetime


if __name__ == '__main__':
    dt = datetime.timedelta(seconds=5)
    moc.tcp_pv(period=10, moc_period=dt)
