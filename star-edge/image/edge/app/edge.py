import os
import time
import json
import random
from threading import Thread

import argparse
import websocket

import serial
import serial.threaded

##################################

CMD_QUERY_DATA = 'data'
CMD_LED_ON = 'led_on'
CMD_LED_OFF = 'led_off'
CMD_PIR_ON = 'pir_on'
CMD_PIR_OFF = 'pir_off'
CMD_UPDATE_PIR = 'update_pir_millis='

##################################

class EdgeService:

    def __init__(self, ws_netloc, ws_path, device_id, device_token, timeout, serial_handler):
        self.device_id = device_id
        self.ws_url = '{}://{}{}{}?token={}'.format(
            'ws', # 'wss' if ws_netloc.split(':')[0] == 'xxx.itlab.ee.ncku.edu.tw'
            ws_netloc, ws_path,
            device_id, device_token
        )
        self.timeout = timeout
        self.serial_handler = serial_handler
        self.poster_handler = None

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
        print("ws connected")
        
        if self.serial_handler is not None:
            self.serial_handler.ws = self.ws

        self.poster_handler = PostInfoHandler(self.ws, self.serial_handler, self.timeout)
        self.poster_handler.start()

    def _on_close(self):
        print("ws disconnected")
        self.poster_handler.die = True

    def _on_error(self, error):
        print("ws error: {}".format(error))

    def _on_message(self, message):
        MessageHandler(self.ws, self.serial_handler, self.device_id, message).start()

##################################

class PostInfoHandler(Thread):
    
    def __init__(self, ws, serial_handler, timeout):
        Thread.__init__(self)
        self.ws = ws
        self.serial_handler = serial_handler
        self.timeout = timeout
        self.die = False
    
    def run(self):
        while not self.die:
            try:
                if self.serial_handler is not None:
                    if self.serial_handler.serail_running:
                        self.serial_handler.write_line(CMD_QUERY_DATA)
                    else:
                        break
                else:
                    self.ws.send(json.dumps({
                        'cmd': 'update_info',
                        'data': self.gen_random_info()
                    }))
            except:
                pass
            
            time.sleep(self.timeout)
        
        print('poster stopped')
        self.ws.close()
    
    def gen_random_info(self):
        return {
            'temperature': round(random.uniform(1,101), 1),
            'humidity': round(random.uniform(1,101), 1),
            'pmat25': round(random.uniform(1,101), 1),
            'loudness': round(random.uniform(1,101), 1),
            'light_intensity': round(random.uniform(1,101), 1),
            'uv_intensity': round(random.uniform(1,101), 1),
            'led_status': random.getrandbits(1),
        }

##################################

class MessageHandler(Thread):

    def __init__(self, ws, serial_handler, device_id, message):
        Thread.__init__(self)
        self.ws = ws
        self.serial_handler = serial_handler
        self.device_id = device_id
        self.ws_msg = json.loads(message)
    
    def run(self):
        try:
            print('ws received: {}'.format(self.ws_msg['cmd']))
            if self.serial_handler is not None:            
                if self.ws_msg['cmd'] == 'led_ctrl':
                    self.serial_handler.write_line(
                        CMD_LED_ON if bool(self.ws_msg['data']['led_status'])
                        else CMD_LED_OFF
                    )
                elif self.ws_msg['cmd'] == 'pir_ctrl':
                    self.serial_handler.write_line(
                        CMD_PIR_ON if bool(self.ws_msg['data']['pir_status'])
                        else CMD_PIR_OFF
                    )
                elif self.ws_msg['cmd'] == 'update_pir_millis':
                    self.serial_handler.write_line(
                        '{}{}'.format(
                            CMD_UPDATE_PIR,
                            self.ws_msg['data']['pir_timeout']
                        )
                    )
        except:
            pass

##################################

class SerialHandler(serial.threaded.LineReader):
    
    def __init__(self):
        super(serial.threaded.LineReader, self).__init__()
        self.ws = None
        self.serail_running = False
        self.latest_data = {}
    
    def __call__(self):
        return self

    def connection_made(self, transport):
        super(SerialHandler, self).connection_made(transport)
        print('serial port opened')
        self.serail_running = True

    def handle_line(self, data):
        try:
            msg = json.loads(data)
            msg_type = msg['type']
            msg_data = msg['content']
            
            print('serial received: {}'.format(msg_type))
            
            self.latest_data.update(msg_data)
            
            self.ws.send(json.dumps({
                'cmd': 'update_info',
                'data': self.latest_data
            }))
        
        except:
            pass

    def connection_lost(self, exc):
        print('serial port closed')
        self.serail_running = False

##################################

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--netloc', help='network location')
    parser.add_argument('--path', help='uri path')
    parser.add_argument('--device', help='device id')
    parser.add_argument('--token', help='token')
    parser.add_argument('--timeout', default=10, help='timeout')
    parser.add_argument('--serial_port', help='Arduino serail port path')
    parser.add_argument('--serial_baud', default=9600, help='Arduino serail baud rate')
    args = parser.parse_args()
    
    try:
        ser = serial.serial_for_url(args.serial_port, baudrate=int(args.serial_baud))
        serial_worker = serial.threaded.ReaderThread(ser, SerialHandler())
        serial_handler = serial_worker.__enter__()
    except:
        print('Fail to connect Serial Port')
        serial_handler = None
    
    try:
        EdgeService(
            args.netloc,
            args.path,
            args.device,
            args.token,
            int(args.timeout),
            serial_handler
        ).start()

        print('EdgeService stopped (waiting for threads stopped)')
    except:
        print("Fail to start EdgeService")
    
    if serial_handler is not None:
        serial_worker.close()

# python -u edge.py --netloc localhost:65001 --path /ws/edge/device/ --device TX2_1 --token ef8a6d2d-cd2c-449f-a455-5d646861b863 --timeout 10 --serial_port /dev/ttyACM0 --serial_baud 9600
