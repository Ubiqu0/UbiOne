# import sys
import asyncio
# import time,logging,json
import serial,time
# import numpy as np
from yamspy import MSPy
from approxeng.input.selectbinder import ControllerResource

FC_SEND_LOOP_TIME = 0.05
CHECK_STATUS = 1
serial_ubione = "/dev/serial0"
DEAD_ZONE = 0.3

CMDS_ORDER = ['roll', 'pitch', 'throttle', 'yaw', 'aux1', 'aux2']
CMDS = {
        'roll':     1500,
        'pitch':    1500,
        'yaw':      1500,
        'aux1':     1000,
        'aux2':     1500
        }

def stick2pwm(x):
    if x > 0:
        x = x-DEAD_ZONE
    elif x < -DEAD_ZONE:
        x = x+DEAD_ZONE
    return int(500*x)


def stick2pwm_throttle(x):
    if x > 0:
        x = x-DEAD_ZONE
    elif x < -DEAD_ZONE:
        x = x+DEAD_ZONE
    return int(800*x)

async def run():
    async with MSPy(device=serial_ubione, logfilename=None, loglevel = 'WARNING',baudrate=115200)as board:
        check_status_time = time.time()
        armed = False
        with ControllerResource() as joystick:
            while joystick.connected:
                #lx -> ga_0
                #ly -> ga_1

                #rx -> ga_2
                #ry -> ga_3
                lx,ly,rx,ry,triangle,rt,lt = joystick['lx','ly','rx','ry','triangle','rt','lt']
                throttle = ly
                yaw = lx
                roll = rx
                pitch = ry

                if throttle > 0:
                    CMDS['throttle'] = 1000+stick2pwm_throttle(throttle)
                else:
                    CMDS['throttle'] = 1000

                if abs(yaw) > DEAD_ZONE:
                    CMDS['yaw'] = 1500+stick2pwm(yaw)
                else:
                    CMDS['yaw'] = 1500

                if abs(roll) > DEAD_ZONE:
                    CMDS['roll'] = 1500+stick2pwm(roll)
                else:
                    CMDS['roll'] = 1500

                if abs(pitch) > DEAD_ZONE:
                    CMDS['pitch'] = 1500+stick2pwm(pitch)
                else:
                    CMDS['pitch'] = 1500

                if rt > 0.9 and CMDS['aux1'] < 1500:
                    CMDS['aux1'] = 1800
                elif lt > 0.9 and CMDS['aux1'] > 1500:
                    CMDS['aux1'] = 1000

                #send cmds to FC
                if await board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER]):
                    dataHandler = await board.receive_msg()
                    await board.process_recv_data(dataHandler)
                #check status
                if (time.time()-check_status_time) >= CHECK_STATUS:
                    # Read info from the FC
                    next_msg = 'MSP_STATUS_EX'
                    temp = await board.send_RAW_msg(MSPy.MSPCodes[next_msg], data=[])
                    if temp:
                        dataHandler = await board.receive_msg()
                        await board.process_recv_data(dataHandler)
                    armed = board.bit_check(board.CONFIG['mode'],0)
                    flags = board.process_armingDisableFlags(board.CONFIG['armingDisableFlags'])
                    flags= ','.join(flags)
                    check_status_time = time.time()
                    print(armed,flags)
                time.sleep(FC_SEND_LOOP_TIME)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
