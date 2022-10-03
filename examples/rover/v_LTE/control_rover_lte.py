import sys
sys.path.append("/home/pi/Ubiquo")
import asyncio
import time,logging,json
from ubirtc.webrtc import WebRTC,GSTWebRTCApp
import serial,time

#
WS_SERVER = 'wss://ubiquo.net/ws/control/'
DEVICE_ID = ''
#
serial_ubione = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# STM32F411 pinout
pm = {'PA0': 192,'PA1': 193,'PA2': 2,'PA3': 3,'PA4': 4,'PA5': 5,'PA6': 6,
           'PA7': 7,'PA8': 8,'PA9': 9,'PA10': 10,'PA11': 11,'PA12': 12,
           'PA13': 13,'PA14': 29,'PA15': 15,'PB0': 16,'PB1': 17,'PB2': 18,
           'PB3': 19,'PB4': 20,'PB5': 21,'PB6': 22,'PB7': 23,'PB8': 24,
           'PB9': 25,'PB10': 26,'PB11': 27,'PB12': 27,'PB13': 28,'PB14': 29,
           'PB15': 30,'PC13': 31,'PC14': 32,'PC15': 33,'PH0': 34,'PH1': 35}

MAX_PULSE = 0.4

class Drive():
    def __init__(self,serial):
        self.serial = serial
        # state: [cmd,pin,hsb,lsb]
        #cmds:
        #    10:attach
        #    15:write ms
        #    20:detach
        #    30:buzz

        self.state = [
            [10,pm['PA0'],5,220],  # main DC motor (1500ms as default)
            [10,pm['PA1'],5,220],  # servo left right (1500ms as default)
            [30,pm['PB14'],0,0],  # servo left right (1500ms as default)
        ]
        self.write_state()
        self.state_changed = True
        self.for_back = 0
        self.left_right = 0.5

    def write_state(self):
        state = [y for x in self.state for y in x]
        self.serial.write(state)
        self.state_changed = False
        #put buzzer back to zero
        self.state[2] = [30,pm['PB14'],0,0]

    def ms2bytes(self,ms):
        bytes = ms.to_bytes(2, 'big')
        return [x for x in bytearray(bytes)]

    def brake(self):
        bts = self.ms2bytes(1500)
        self.for_back = 0
        self.state[0] = [15,pm['PA0']] + bts
        self.state_changed = True

    def mv_for_back(self,rt):
        ms = int(1500+500*rt)
        self.for_back = rt/MAX_PULSE
        bts = self.ms2bytes(ms)
        self.state[0] = [15,pm['PA0']] + bts
        self.state_changed = True

    def mv_left(self):
        bts = self.ms2bytes(1800)
        self.left_right = 0.2
        self.state[1] = [15,pm['PA1']] + bts
        self.state_changed = True

    def mv_right(self):
        #fixed PWM for left
        bts = self.ms2bytes(1200)
        self.left_right = 0.8
        self.state[1] = [15,pm['PA1']] + bts
        self.state_changed = True

    def mv_center(self):
        bts = self.ms2bytes(1500)
        self.left_right = 0.5
        self.state[1] = [15,pm['PA1']] + bts
        self.state_changed = True

    def buzzer(self):
        bts = self.ms2bytes(2000)
        self.state[2] = [30,pm['PB14']] + bts
        self.state_changed = True

    def detach(self):
        self.state[0] = [20,pm['PA0'],0,0]
        self.state[1] = [20,pm['PA1'],0,0]
        self.state_changed = True

# define what to do with the received messages
class GstApp(GSTWebRTCApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = Drive(serial_ubione)

    async def on_data_message(self,msg):
        #message received in the data channel
        msg = json.loads(msg)
        if 'ga_1' not in msg:
            if msg['w']['pressed'] and not msg['s']['pressed']:
                print("received move mv_forward",time.time())
                self.driver.mv_for_back(0.5*MAX_PULSE)
                pass
            elif not msg['w']['pressed'] and msg['s']['pressed']:
                self.driver.mv_for_back(-0.5*MAX_PULSE)
                pass
            else:
                self.driver.brake()
                pass

            if msg['a']['pressed'] and not msg['d']['pressed']:
                self.driver.mv_right()
                pass
            elif not msg['a']['pressed'] and msg['d']['pressed']:
                self.driver.mv_left()
                pass
            else:
                self.driver.mv_center()
                pass

        if 'ga_1' in msg and msg['ga_1']['pressed']:
            ga_1 = float(msg['ga_1']['value'])
            if ga_1 < -0.1 or ga_1 > 0.1:
                self.driver.mv_for_back(-ga_1*MAX_PULSE)
            else:
                self.driver.brake()
        elif 'ga_1' in msg and not msg['ga_1']['pressed']:
            self.driver.brake()

        if 'ga_2' in msg and msg['ga_2']['pressed']:
            ga_2 = float(msg['ga_2']['value'])
            if ga_2 > 0.5:
                self.driver.mv_right()
            elif ga_2 < -0.5:
                self.driver.mv_left()
            else:
                self.driver.mv_center()
        elif 'ga_2' in msg and not msg['ga_2']['pressed']:
            self.driver.mv_center()

        if 'gb_6' in msg and float(msg['gb_6']['value']) > 0.9:
            self.driver.buzzer()

        if self.driver.state_changed:
            self.driver.write_state()


async def send_data_message(gst_app):
    count = 0
    while True:
        await asyncio.sleep(0.1)
        if gst_app.is_data_channel_ready():
            ###########################
            ######## add your code here
            #########################
            # send dictionary with t1,t2,...,t8 as keys and the respective value with the format ['name',value]
            # If you want a progressive you can send the min and max with ['name',value,min,max]
            data = {}
            if gst_app.driver.for_back > 0:
                vel = 100*gst_app.driver.for_back
                vel = int(vel)
                data['t1'] = ['Vel',vel,0,100]
            else:
                data['t1'] = ['Vel',0,0,1]

            data['t2'] = ['Left-Right',gst_app.driver.left_right,0,1]


            ###########################
            ###########################
            gst_app.send_data_message('telemetry',data)


async def run():
    webrct_connection = WebRTC(
                            DEVICE_ID,
                            WS_SERVER,
                            app = GstApp(audio = True)
                        )
    asyncio.ensure_future(send_data_message(webrct_connection.app))
    await webrct_connection.connect()
    await webrct_connection.start()


if __name__ == "__main__":

    import os
    try:
        with open('~/.asoundrc') as f:
            pass
    except Exception as e:
        os.system('cp ~/.asoundrc_bck ~/.asoundrc')


    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling loop...")
        loop.close()
