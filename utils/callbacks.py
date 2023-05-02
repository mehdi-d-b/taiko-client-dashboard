import pandas as pd
import orjson as json
from tornado import gen

# Set up callback with streaming data
@gen.coroutine
def sin_data(**kwargs):
    # Read the last element from the Redis list
    data = kwargs['r'].lindex('random_sin', -1)
    if data:
        data = json.loads(data)
        index = pd.to_datetime(data['timestamp'], unit='ms')
        return pd.DataFrame({'var_0': data['var_0'],
                           'var_1': data['var_1'],
                           'var_2': data['var_2'],
                           'var_3': data['var_3'],
                           'var_4': data['var_4'],
                           'var_5': data['var_5'],
                           'var_6': data['var_6'],
                           'var_7': data['var_7']},
                          columns=['var_' + str(x) for x in range(8)], index=[index])