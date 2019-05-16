import os
import time
import json
import random
from threading import Thread

import argparse
import websocket

##################################

class CloudConnector:

    def __init__(self, ws_netloc, ws_path, device_id, device_token, timeout):
        self.device_id = device_id
        self.ws_url = '{}://{}{}{}?token={}'.format(
            'ws', # 'wss' if ws_netloc.split(':')[0] == 'xxx.itlab.ee.ncku.edu.tw'
            ws_netloc, ws_path,
            device_id, device_token
        )
        self.timeout = timeout

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message = self._on_message,
            on_open = self._on_open,
            on_error = self._on_error,
            on_close = self._on_close
        )

        self.ws.run_forever()
    
    def _on_open(self):
        print("{} ... connected".format(self.device_id))
        PostInfoHandler(self.ws, self.timeout).start()

    def _on_close(self):
        print("{} ... disconnected".format(self.device_id))

    def _on_error(self, error):
        print("{} ... error: {}".format(self.device_id, error))

    def _on_message(self, message):
        MessageHandler(self.ws, self.device_id, message).start()

##################################

class PostInfoHandler(Thread):
    def __init__(self, ws, timeout):
        Thread.__init__(self)
        self.ws = ws
        self.timeout = timeout
    
    def run(self):
        try:
            while True:
                raw = {
                    'cmd': 'update_info',
                    'data': self._get_info()
                }
                self.ws.send(json.dumps(raw))
                time.sleep(self.timeout)
        except:
            pass

    def _get_info(self):
        return {
            'temperature': round(random.uniform(1,101), 1),
            'humidity': round(random.uniform(1,101), 1),
            'pm2_5': round(random.uniform(1,101), 1),
            'loudness': round(random.uniform(1,101), 1),
            'light_intensity': round(random.uniform(1,101), 1),
            'uv_intensity': round(random.uniform(1,101), 1),
            'ir_sensed': bool(random.getrandbits(1)),
        }

##################################

class MessageHandler(Thread):

    def __init__(self, ws, device_id, message):
        Thread.__init__(self)
        self.ws = ws
        self.device_id = device_id
        self.message = json.loads(message)
    
    def run(self):
        if self.message['cmd'] == 'update_info':
            print('{} Recv {}'.format(self.device_id, self.message['data']))

if __name__ == "__main__":
    # websocket.enableTrace(True)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--netloc', help='network location')
    parser.add_argument('--path', help='uri path')
    parser.add_argument('--device', help='device id')
    parser.add_argument('--token', help='token')
    parser.add_argument('--timeout', type=int, default=10, help='timeout')
    args = parser.parse_args()

    while True:
        try:
            CloudConnector(
                args.netloc,
                args.path,
                args.device,
                args.token,
                args.timeout
            ).start()
            time.sleep(args.timeout)
        except:
            print("{} ... disconnected".format(os.getenv('DEVICE')))
            time.sleep(args.timeout)