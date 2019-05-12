import pandas as pd
import numpy as np

def build_tree_struct(data):
    def crypt_lambda(x):
        # print(x)
        iden = x['identifier']
        crypt_row = ''
        if 'BU' in iden:
            crypt_row = 'BU'
        elif 'ETU' in iden:
            crypt_row = 'ETU'
        elif 'ETB' in iden:
            crypt_row = 'ETB'
        elif 'EOU' in iden:
            crypt_row = 'EOU'
        elif 'EOB' in iden:
            crypt_row = 'EOB'
        else:
            return None
        return crypt_row

    def level_lambda(x):
        iden = x['identifier']
        level_of_stakana = iden[-1]
        if not level_of_stakana.isnumeric():
            return None
        return int(level_of_stakana)

    def operation_lambda(x):
        iden = x['identifier']
        operation = iden[-2]
        if operation not in 'czxe':
            return None
        return operation
    
    data['crypt'] = data.apply(crypt_lambda, axis=1)
    data['level'] = data.apply(level_lambda, axis=1)
    data['operation'] = data.apply(operation_lambda, axis=1)
    data = data.dropna()
    print('1 этап пройден')
    
    time_batch = data.groupby(['timestamp'])
    end_data = {}

    """
    0         1              2      3      4     5
    timestamp identifier     amount crypt  level operation
    """

    for ind  in time_batch.groups.values():
        # print(counter)

        group = batch.loc[ind].values
        time = group[0][0]
        market_time = {}
        end_data[time]  = market_time

        unique_crypt = np.unique(group[:, 3])
        for concrete_crypt in unique_crypt:
            concrete_crypt_group = group[group[:, 3] == concrete_crypt]

            market_crypt = {}
            market_time[concrete_crypt] = market_crypt

            # лучший уровень стакана
            level = np.min(concrete_crypt_group[:, 4])

            market_crypt['level'] = level

            concrete_crypt_group = concrete_crypt_group[concrete_crypt_group[:, 4] == level]

            unique_oper = np.unique(concrete_crypt_group[:, 5])
            for concrete_oper in unique_oper:
                czex = concrete_crypt_group[concrete_crypt_group[:, 5] == concrete_oper]
                czex = np.array(czex[:, 2], dtype=np.float)
                # concrete oper - c/z/e/x
                # value to write
                market_crypt[concrete_oper] = czex.mean()
    print('2 этап пройден')
    return end_data
    
    
    
if __name__ == '__main__':
    path = f'data/md_reb_track\\34_day0.csv'
    df = pd.read_csv(path)
    df = df.dropna()
    print('Начальная длина', df.shape)
    batch = df[:100000]
    data = build_tree_struct(batch)
    print(len(data))
    print(data)
