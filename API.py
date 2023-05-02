import time
import redis
import json
import math
import random
from flask import Flask, request
import threading

NOMBRE_DE_POINTS = 1000

app = Flask(__name__)
redis_client = redis.Redis()

sine_params = {'freq': 1.0, 'amplitude': 1.0, 'noise_amplitude': 0.1}

def generate_data():
    while True:
        timestamp = int(time.time() * 1000)
        sine_data = {'timestamp': timestamp}
        for i in range(8):
            sine_var = 'var_{}'.format(i)
            sine_val = float(sine_params['amplitude']) * math.sin(float(sine_params['freq'] + i/5.0) * timestamp / 1000.0) + i
            sine_val += random.uniform(-sine_params['noise_amplitude'], sine_params['noise_amplitude'])
            sine_data[sine_var] = sine_val
        # Enum
        ts = (timestamp % 60000) / 1000
        if ts % 10 < 3:
            sine_data['enum'] = 0
        elif ts % 2 == 0:
            sine_data['enum'] = 1
        else:
            sine_data['enum'] = 2
        
        redis_client.rpush('random_sin', json.dumps(sine_data))

        if redis_client.llen('random_sin') >= NOMBRE_DE_POINTS:
            redis_client.lpop('random_sin')

        time.sleep(0.1)

@app.route('/set_sine_params', methods=['POST'])
def set_sine_params():
    data = request.get_json()
    sine_params['freq'] = data.get('freq', sine_params['freq'])
    sine_params['amplitude'] = data.get('amplitude', sine_params['amplitude'])
    sine_params['noise_amplitude'] = data.get('noise_amplitude', sine_params['noise_amplitude'])
    return 'Sine parameters updated'


if __name__ == '__main__':
    generator_thread = threading.Thread(target=generate_data)
    generator_thread.start()
    app.run()
