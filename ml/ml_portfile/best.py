class MomentCosts:
    def __init__(self, val=None):
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
        val['BTE'] = 1/val['ETB']
        #val['UEO'] = 1/val['EOU']
        val['BEO'] = 1/val['EOB']
        self.val = val

    def get_cost(self, l, r):
        if l == r:
            return 1
        if l+r in self.val:
            return self.val[l+r]
        return -1

    def __str__(self):
        return str(self.val)


def get_best_value(cost_gener, start_val=None):
    if start_val is None:
        start_val = {'B': 0.1, 'U': float('inf'), 'ET': float('inf'), 'EO': float('inf')}
    val = ['B', 'U', 'EO']
    for mc in cost_gener:
        old = start_val.copy()
        for nfield in val:
            for ofield in val:
                t = mc.get_cost(ofield, nfield)
                if t != -1:
                    start_val[nfield] = min(start_val[nfield], old[ofield]/t)
    return 1/start_val['B']


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
