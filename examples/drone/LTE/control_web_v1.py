import sys
sys.path.append("/home/pi/Ubiquo")
import asyncio
import time,logging,json
from ubirtc.webrtc import WebRTC,GSTWebRTCApp
import serial,time
import numpy as np
from yamspy_async import MSPy

#
WS_SERVER = 'wss://ubiquo.net/ws/control/'
DEVICE_ID = '' #insert your device ID

SERIAL_UBIONE = "/dev/serial0"
CMDS_ORDER = ['roll', 'pitch', 'throttle', 'yaw', 'aux1', 'aux2']
CMDS_STEP = 25

class GstApp(GSTWebRTCApp):
    def __init__(self, board,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.CMDS = {
                'roll':     1500,
                'pitch':    1500,
                'throttle': 900,
                'yaw':      1500,
                'aux1':     1000,
                'aux2':     1000,
                'aux3':     1000,
                'aux4':     1000
                }
        self.last_msg_received = time.time()
        self.received_cmd = False


    def stick2pwm(self,x):
        # return int(1500+200*x)
        return int(1500+400*x)


    async def on_data_message(self,msg):
        #message received in the data channel
        msg = json.loads(msg)
        self.last_msg_received = time.time()
        # print("Start received msg",self.last_msg_received)
        ###############
        ###### mechanics from the PS4 controller to UbiOne
        # gb_0 -> X
        # gb_1 -> Circle
        # gb_2 -> Square
        # gb_3 -> triangle
        # gb_4 -> L1
        # gb_5 -> R1
        # gb_6 -> L2
        # gb_7 -> R2
        # gb_8 -> Share
        # gb_9 -> Options
        # gb_10 -> L3
        # gb_11 -> R3
        # gb_12 -> Dpad up
        # gb_13 -> Dpad down
        # gb_14 -> Dpad left
        # gb_15 -> Dpad right
        # gb_16 -> PS
        # gb_17 -> Touchpad
        # ga_0 -> Left Stick left and right
        # ga_1 -> Left Stick up and down
        # ga_2 -> Right Stick left and right
        # ga_3 -> Right Stick up and down
        ###############
        # now = time.time()

        # print(msg)
        if 'gb_6' in msg and float(msg['gb_6']['value']) > 0.9:
            print("disarm")
            self.CMDS['aux1'] = 1000
        elif 'gb_7' in msg and float(msg['gb_7']['value']) > 0.9:
            print("arm")
            self.CMDS['aux1'] = 1800

        if 'ga_3' in msg:
            pitch = -1.0*float(msg['ga_3']['value'])
            # print(pitch,type(pitch))
        else:
            pitch = 0
        if 'ga_2' in msg:
            roll = float(msg['ga_2']['value'])
        else:
            roll = 0
        if 'ga_1' in msg:
            thro = float(msg['ga_1']['value'])
        else:
            thro = 0
        if 'ga_0' in msg:
            yaw = float(msg['ga_0']['value'])
        else:
            yaw = 0

        if 'ga_3' in msg and abs(pitch) > 0.3:
            self.CMDS['pitch'] = self.stick2pwm(pitch)
        elif 'ga_3' in msg and msg['ga_3']['pressed'] == False:
            self.CMDS['pitch'] = 1500

        if 'ga_2' in msg and abs(roll) > 0.3:
            self.CMDS['roll'] = self.stick2pwm(roll)
        elif 'ga_2' in msg and msg['ga_2']['pressed'] == False:
            self.CMDS['roll'] = 1500

        if 'ga_0' in msg and abs(yaw) > 0.3:
            self.CMDS['yaw'] = self.stick2pwm(yaw)
        elif 'ga_0' in msg and msg['ga_0']['pressed'] == False:
            self.CMDS['yaw'] = 1500

        # for throttle we a simple add and subtract
        if 'ga_1' in msg and thro < -0.5:
            self.CMDS['throttle'] = self.CMDS['throttle'] + CMDS_STEP if self.CMDS['throttle'] + CMDS_STEP <= 2000 else self.CMDS['throttle']
        elif 'ga_1' in msg and thro > 0.5:
            self.CMDS['throttle'] = self.CMDS['throttle'] - CMDS_STEP if self.CMDS['throttle'] - CMDS_STEP >= 1000 else self.CMDS['throttle']


        # if 'gb_3' in msg and msg['gb_3']['pressed']:
        #     self.CMDS = {
        #             'roll':     1500,
        #             'pitch':    1500,
        #             'throttle': 900,
        #             'yaw':      1500,
        #             'aux1':     1000,
        #             'aux2':     1000
        #             }
        #     await self.board.reboot()
            # self.msp_status()
        if 'gb_1' in msg and msg['gb_1']['pressed']:
            print("reset")
            self.CMDS = {
                    'roll':     1500,
                    'pitch':    1500,
                    'throttle': 900,
                    'yaw':      1500,
                    'aux1':     1000,
                    'aux2':     1000,
                    'aux3':     1000,
                    'aux4':     1000
                    }

        self.received_cmd = True

# FC_SEND_LOOP_TIME mut be smaller than UBI_SEND_LOOP_TIME
FC_SEND_LOOP_TIME = 0.05
CHECK_STATUS = 1

async def fc_loop(gst_app):
    check_status_time = time.time()
    armed = 0
    flags = ''
    altitude = 0
    voltage = 0
    while True:
        await asyncio.sleep(FC_SEND_LOOP_TIME)
        #send cmds to FC and check if cmds is beeing received
        if gst_app.received_cmd and await gst_app.board.send_RAW_RC([gst_app.CMDS[ki] for ki in CMDS_ORDER]):
            dataHandler = await gst_app.board.receive_msg()
            await gst_app.board.process_recv_data(dataHandler)
            gst_app.received_cmd = False #safeguard to make sure data is beeing received from control room

        #check status
        if (time.time()-check_status_time) >= CHECK_STATUS:
            # Read info from the FC
            next_msg = 'MSP_STATUS_EX'
            temp = await gst_app.board.send_RAW_msg(MSPy.MSPCodes[next_msg], data=[])
            if temp:
                dataHandler = await gst_app.board.receive_msg()
                await gst_app.board.process_recv_data(dataHandler)
            armed = gst_app.board.bit_check(gst_app.board.CONFIG['mode'],0)
            flags = gst_app.board.process_armingDisableFlags(gst_app.board.CONFIG['armingDisableFlags'])
            await gst_app.board.fast_read_altitude()
            await gst_app.board.fast_read_analog()
            altitude = gst_app.board.SENSOR_DATA['altitude']
            voltage = gst_app.board.ANALOG['voltage']
            flags= ','.join(flags)
            check_status_time = time.time()
            print(armed,flags)


        #send telemetry
        if gst_app.is_data_channel_ready():

            # send dictionary with t1,t2,...,t8 as keys
            # and the respective list of values where ['name',value,min,max]
            # Note: if you do not want a progressive bar then just send the array ['name',value]

            data = {
                't1':['ARMED',1 if armed else 0,0,1],
                't2':['Flags',flags],
                't3':['throttle',gst_app.CMDS['throttle'],1000,2000],
                't4':['yaw',gst_app.CMDS['yaw'],1000,2000],
                't5':['pitch',gst_app.CMDS['pitch'],1000,2000],
                't6':['roll',gst_app.CMDS['roll'],1000,2000],
                't7':['altitude',altitude,0,100],
                't8':['voltage',voltage,7,12.3]

                }
            gst_app.send_data_message('telemetry',data)


async def run():

    pipeline_str  = ''' webrtcbin name=sendrecv bundle-policy=max-bundle
    v4l2src device=/dev/video0 !
    video/x-h264,profile=constrained-baseline,width=1280,height=720,level=3.0,framerate=30/1 !
    queue max-size-time=100000000 ! h264parse !
    rtph264pay mtu=1024 config-interval=-1 name=payloader !
    capssetter caps=\"application/x-rtp,profile-level-id=42c028,encoding-name=H264,payload=96\" ! sendrecv.'''

    async with MSPy(device=SERIAL_UBIONE, logfilename=None, loglevel = 'WARNING',baudrate=115200)as ubione:
        command_list = ['MSP_API_VERSION', 'MSP_FC_VARIANT', 'MSP_FC_VERSION', 'MSP_BUILD_INFO',
                        'MSP_BOARD_INFO', 'MSP_UID', 'MSP_ACC_TRIM', 'MSP_NAME', 'MSP_STATUS',
                        'MSP_STATUS_EX','MSP_BATTERY_CONFIG', 'MSP_BATTERY_STATE', 'MSP_BOXNAMES']
        for msg in command_list:
            if await ubione.send_RAW_msg(MSPy.MSPCodes[msg], data=[]):
                dataHandler = await ubione.receive_msg()
                await ubione.process_recv_data(dataHandler)

        webrct_connection = WebRTC(
                                DEVICE_ID,
                                WS_SERVER,
                                app = GstApp(board = ubione,audio = False, pipeline_str = pipeline_str)
                            )
        asyncio.ensure_future(fc_loop(webrct_connection.app))

        await webrct_connection.connect()
        await webrct_connection.start()


if __name__ == "__main__":
    #start GPS

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.close()
    except Exception as e:
        print("Caught exception: %s" % e)
