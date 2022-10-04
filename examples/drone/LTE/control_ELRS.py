import asyncio
import time,logging,json
import serial
import sys,re
sys.path.insert(0, '/home/pi/Ubiquo')
from ubirtc.webrtc import WebRTC,GSTWebRTCApp
from yamspy_async import MSPy
from cellulariot import cellulariot

WS_SERVER = 'wss://ubiquo.net/ws/control/'
DEVICE_ID = '' #insert your device ID
SERIAL_UBIONE = "/dev/serial0"

def parse_sig_q(response):
    x = re.search(r'CSQ: \d+,\d+',response)
    if x:
        x = x.group().replace('CSQ:','').strip()
        q = x.split(',')[0]
        q = int(q)
        return q
    else:
        return 0

class GstApp(GSTWebRTCApp):
    def __init__(self, board,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.last_msg_received = time.time()
        self.received_cmd = False


SEND_TIME_INTERVAL = 1
async def send_data_message(gst_app):
    count = 0
    # SERIAL_LTE = aioserial.AioSerial("/dev/ttyUSB2", baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)
    node = cellulariot.CellularIoT(serial_port="/dev/ttyUSB2")

    while True:
        await asyncio.sleep(SEND_TIME_INTERVAL)
        if gst_app.is_data_channel_ready():
            ###########################
            ######## add your code here
            #########################
            # send dictionary with t1,t2,...,t8 as keys and the respective value with the format ['name',value]
            # If you want a progressive bar you can send the min and max with ['name',value,min,max]

            armed = gst_app.board.bit_check(gst_app.board.CONFIG['mode'],0)
            flags = gst_app.board.process_armingDisableFlags(gst_app.board.CONFIG['armingDisableFlags'])
            await gst_app.board.fast_read_altitude()
            await gst_app.board.fast_read_analog()
            altitude = gst_app.board.SENSOR_DATA['altitude']
            voltage = gst_app.board.ANALOG['voltage']

            node.getSignalQuality()
            sig_q = parse_sig_q(node.response)

            flags= ','.join(flags)
            check_status_time = time.time()
            print(armed,flags)

            data = {
                't1':['ARMED',1 if armed else 0,0,1],
                't2':['Flags',flags],
                't3':['altitude',altitude,0,100],
                't4':['voltage',voltage],
                't5':['Signal',sig_q,0,31],

                }
            count+=1

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
        asyncio.ensure_future(send_data_message(webrct_connection.app))

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
