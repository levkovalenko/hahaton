import datetime
import collections


class MomentCosts:
    def __init__(self, date, val=None):
        if val is None:
            val = {
            'BU': 1,
            #'ETU': 1,
            'ETB': 1,
            #'EOU': 1,
            'EOB': 1
        }
        val['UB'] = 1/val['BU']
        #val['UET'] = 1/val['ETU']
        val['BET'] = 1/val['ETB']
        #val['UEO'] = 1/val['EOU']
        val['BEO'] = 1/val['EOB']
        self.val = val
        self.date = date

    def get_cost(self, l, r):
        if l == r:
            return 1
        if l+r in self.val:
            return self.val[l+r]
        return -1

    def __str__(self):
        return str(self.val)


def get_best_value(cost_gener, period, start_val=None):
    if start_val is None:
        start_val = {'B': 0.1, 'U': float('inf'), 'ET': float('inf'), 'EO': float('inf')}
    val = ['B', 'U', 'EO', 'ET']
    deq = collections.deque()
    pred = dict()
    sm = dict()
    prev = None
    for mc in cost_gener:
        pred[mc.date] = {'B': ('B', prev), 'U': ('U', prev), 'EO': ('EO', prev), 'ET': ('ET', prev)}
        prev = mc.date
        deq.append((start_val.copy(), mc))
        while deq[0][1].date + period < mc.date:
            cmc = deq[0][1]
            old = deq[0][0].copy()
            deq.popleft()
            for nfield in val:
                for ofield in val:
                    t = cmc.get_cost(ofield, nfield)
                    if t != -1 and old[ofield]/t < start_val[nfield]:
                        start_val[nfield] = old[ofield]/t
                        pred[mc.date][nfield] = (ofield, cmc.date)
            #print(start_val)
        sm[mc.date] = {'B': (1/start_val['B'], start_val['B']), 'U': (1/start_val['U']*mc.get_cost('U', 'B'), start_val['U']),
                       'EO': (1/start_val['EO']*mc.get_cost('EO', 'B'), start_val['EO']), 'ET': (1/start_val['ET']*mc.get_cost('ET', 'B'), start_val['ET'])}
    res = collections.deque()
    q = 'B'
    key = prev
    res.append((q, key, sm[key][q][0], 1/sm[key][q][1]))
    while key is not None:
        if len(res) == 1 or res[-1][0] != q:
            res.append((q, key, sm[key][q][0], 1/sm[key][q][1]))
        if res[-1][0] == q:
            res[-1] = (res[-1][0], key, res[-1][2], res[-1][3])
        q, key = pred[key][q]
    return 1/start_val['B'], list(res)[::-1]


if __name__ == '__main__':
    l1 = [0.0575, 0.126, 1.489]
    l2 = [0.1359, 0.86, 1.182]
    l3 = [0.0228, 1.135, 1.343]

    t1 = MomentCosts(val={
            'BU': l1[1],
            'ETU': 100000,
            'ETB': 100000,
            'EOU': l1[2],
            'EOB': 1/l1[0]
        })
    t2 = MomentCosts(val = {
            'BU': l2[1],
            'ETU': 100000,
            'ETB': 100000,
            'EOU': l2[2],
            'EOB': 1/l2[0]
        })
    t3 = MomentCosts(val = {
            'BU': l3[1],
            'ETU': 100000,
            'ETB': 100000,
            'EOU': l3[2],
            'EOB': 1/l3[0]
        })
    print(get_best_value([t1, t2, t3]))
    assert(abs(59.6053 - get_best_value([t1, t2, t3])) < 0.01)
