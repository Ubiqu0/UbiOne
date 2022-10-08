import asyncio
import serial
import time
import subprocess
from approxeng.input.selectbinder import ControllerResource


serial_ubione = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

LOOP_TIME = 0.05



# STM32F411 pinout
pm = {'PA0': 192,'PA1': 193,'PA2': 2,'PA3': 3,'PA4': 4,'PA5': 5,'PA6': 6,
           'PA7': 7,'PA8': 8,'PA9': 9,'PA10': 10,'PA11': 11,'PA12': 12,
           'PA13': 13,'PA14': 29,'PA15': 15,'PB0': 16,'PB1': 17,'PB2': 18,
           'PB3': 19,'PB4': 20,'PB5': 21,'PB6': 22,'PB7': 23,'PB8': 24,
           'PB9': 25,'PB10': 26,'PB11': 27,'PB12': 27,'PB13': 28,'PB14': 29,
           'PB15': 30,'PC13': 31,'PC14': 32,'PC15': 33,'PH0': 34,'PH1': 35}


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

    def write_state(self):
        state = [x for l in self.state for x in l]
        self.serial.write(state)
        self.state_changed = False
        #put buzzer back to zero
        self.state[2] = [30,pm['PB14'],0,0]

    def ms2bytes(self,ms):
        bytes = ms.to_bytes(2, 'big')
        return [x for x in bytearray(bytes)]

    def brake(self):
        bts = self.ms2bytes(1500)
        self.state[0] = [15,pm['PA0']] + bts
        self.state_changed = True

    def mv_for_back(self,rt):
        ms = int(1500+500*rt)
        bts = self.ms2bytes(ms)
        self.state[0] = [15,pm['PA0']] + bts
        self.state_changed = True

    def mv_left(self):
        bts = self.ms2bytes(1800)
        self.state[1] = [15,pm['PA1']] + bts
        self.state_changed = True

    def mv_right(self):
        bts = self.ms2bytes(1200)
        self.state[1] = [15,pm['PA1']] + bts
        self.state_changed = True

    def mv_center(self):
        bts = self.ms2bytes(1500)
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


async def run():
    driver = Drive(serial_ubione)
    with ControllerResource() as joystick:
        MAX_PULSE = 0.5
        while joystick.connected:
            ly,rx,triangle,dup,ddown = joystick['ly','rx','triangle','dup','ddown']
            if dup and dup > 0 and not ddown:
                MAX_PULSE += 0.025
                if MAX_PULSE >= 1:
                    MAX_PULSE = 1
            elif ddown and ddown > 0 and not dup:
                MAX_PULSE -= 0.05
                if MAX_PULSE < 0.1:
                    MAX_PULSE = 0.1
            if ly > 0.1 or ly < -0.1:
                driver.mv_for_back(ly*MAX_PULSE)
            else:
                driver.brake()

            if rx > 0.5:
                driver.mv_right()
            elif rx < -0.5:
                driver.mv_left()
            else:
                driver.mv_center()

            if triangle:
                driver.buzzer()

            if driver.state_changed:
                driver.write_state()


            time.sleep(LOOP_TIME)

if __name__ == '__main__':

    result = subprocess.run(['/bin/bash', 'pair_ps4.sh'], stdout=subprocess.PIPE)
    # print(result.stdout.decode)
    result = result.stdout.decode()
    print(result)
    if 'already connected' in result:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(run())
        except KeyboardInterrupt as e:
            print("Caught keyboard interrupt. Canceling loop...")
            loop.close()
    else:
        subprocess.run(['/bin/bash', 'pair_ps4.sh'], stdout=subprocess.PIPE)
