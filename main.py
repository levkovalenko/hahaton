import api_source.base_sender as sender
import datetime
import ml.ml_portfile.best as best
import csv
import time
import ast
import numpy as np


def generate(file):
    with open(file) as f_in:
        r = csv.reader(f_in)
        names = next(r)
        print(names)
        t = 0
        prev = None
        for line in r:
            q = datetime.datetime.strptime(line[-1], '%Y:%m:%d:%H:%M:%S.%f')
            #if prev is None or prev != line[-1].split(':')[3]:
            #    prev = line[-1].split(':')[3]
            #print(t, line)
            mc = best.MomentCosts(q, val={
                'BU': (float(line[0])+float(line[1]))/2,
                'ETB': (float(line[4]) + float(line[5]))/2,
                'EOB': (float(line[2])+float(line[3]))/2
            })
            yield mc
            t = t+1
            #if t > 50000:
            #    break


def best_bucket():
    val, l = best.get_best_value(generate('data/0.csv'), datetime.timedelta(hours=1))
    print(val)
    tmpd = {'U': 0, 'B': 0, 'ET': 0, 'EO': 0}
    s = sender.TCPSender(ip='172.20.197.19', port=9090)
    for elem in l:
        data = tmpd.copy()
        data[elem[0]] = elem[3]
        data['sum'] = elem[2]
        s.send_bucket(data=data, time=elem[1])
        time.sleep(1)


def read_and_send():
    with open('data/file0.7059.txt') as f_in:
        q = f_in.read()
        data = ast.literal_eval(q)
        print(data.keys())
    s = sender.TCPSender(ip='172.20.197.19', port=9090)
    dd = {
        'y_pred': [],
        'y_test': []
    }
    for i in range(0, len(data['y_pred']), 80):
        if i + 80 > len(data['y_pred']):
            dd['y_pred'].append(np.average(data['y_pred'][i:]))
            dd['y_test'].append(np.average(data['y_test'][i:]))
        else:
            dd['y_pred'].append(np.average(data['y_pred'][i:i+80]))
            dd['y_test'].append(np.average(data['y_test'][i:i+80]))

        if len(dd['y_pred']) >= 20:
            s.send_volatility(data=dd)
            dd = {
                'y_pred': [],
                'y_test': []
            }
            time.sleep(0.5)
    if len(dd['y_pred']) > 0:
        s.send_volatility(data=dd)


def read_bucket_and_send():
    with open('data/final_portfel.csv') as f_in:
        r = csv.reader(f_in)
        names = next(r)
        print(names)
        s = sender.TCPSender(ip='172.20.197.19', port=9090)
        for line in r:
            data = {
                'sum': line[1],
                'BU': line[2],
                'EOB': line[3],
                'ETB': line[4]
            }
            s.send_bucket(data=data)
            time.sleep(1)


def many_write():
    with open('data/file0.7059.txt') as f_in:
        q = f_in.read()
        data = ast.literal_eval(q)
        print(data.keys())
    s = sender.TCPSender(ip='172.20.197.19', port=9090)
    dd = {
        'y_pred': [],
        'y_test': []
    }
    with open('data/final_portfel.csv') as f_in:
        r = csv.reader(f_in)
        names = next(r)
        print(names)
        for i in range(0, len(data['y_pred']), 80):
            if i + 80 > len(data['y_pred']):
                dd['y_pred'].append(np.average(data['y_pred'][i:]))
                dd['y_test'].append(np.average(data['y_test'][i:]))
            else:
                dd['y_pred'].append(np.average(data['y_pred'][i:i + 80]))
                dd['y_test'].append(np.average(data['y_test'][i:i + 80]))

            if len(dd['y_pred']) >= 20:
                s.send_volatility(data=dd)
                dd = {
                    'y_pred': [],
                    'y_test': []
                }
                time.sleep(0.5)
                try:
                    line = next(r)
                    data2 = {
                        'sum': line[1],
                        'BU': line[2],
                        'EOB': line[3],
                        'ETB': line[4]
                    }
                    s.send_bucket(data=data2)
                    time.sleep(0.5)
                except Exception:
                    pass

        if len(dd['y_pred']) > 0:
            s.send_volatility(data=dd)


def main():
    #print(best.get_best_value(generate('data/0.csv'), datetime.timedelta(hours=1)))
    #read_bucket_and_send()
    #read_and_send()
    many_write()


if __name__ == '__main__':
    #dt = datetime.timedelta(seconds=4)
    #moc.tcp_bucket(period=4, moc_period=dt, ip='172.20.197.19')
    #moc.tcp_pv(period=10, moc_period=dt)
    #best_bucket()
    main()
