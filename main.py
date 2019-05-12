import api_source.mocs as moc
import datetime
import ml.ml_portfile.best as best
import csv


def generate(file):
    with open(file) as f_in:
        r = csv.reader(f_in)
        names = next(r)
        print(names)
        t = 0
        prev = None
        for line in r:
            if prev is None or prev != line[-1].split(':')[3]:
                prev = line[-1].split(':')[3]
                print(t, prev, line)
                mc = best.MomentCosts(val={
                    'BU': (float(line[0])+float(line[1]))/2,
                    'ETB': (float(line[4]) + float(line[5]))/2,
                    'EOB': (float(line[2])+float(line[3]))/2
                })
                yield mc
            t = t+1
#            if t > 50000:
#                break


def main():
    print(best.get_best_value(generate('data/0.csv')))


if __name__ == '__main__':
    #dt = datetime.timedelta(seconds=4)
    #moc.tcp_bucket(period=4, moc_period=dt, ip='172.20.197.19')
    #moc.tcp_pv(period=10, moc_period=dt)
    main()
