#include <CrsfSerial.h>
#include <Servo.h>

HardwareSerial Modem(USART1);

Servo servo[2];
int ch1,ch2,ch3,ch4,ch5;

CrsfSerial crsf(Modem, CRSF_BAUDRATE); // pass any HardwareSerial port

/***
 * This callback is called whenever new channel values are available.
 * Use crsf.getChannel(x) to get us channel values (1-16).
 ***/
void packetChannels()

{
  ch1 = crsf.getChannel(1);
  ch2 = crsf.getChannel(2);
  ch3 = crsf.getChannel(3);
  ch4 = crsf.getChannel(4);
  ch5 = crsf.getChannel(5);

  if (ch4 > 1500){
    if (ch4 > 2000){
      ch4 = 2000;
    }
    ch4 = 1500-(2000-ch4);
  } else{
    if (ch4 < 1000){
      ch4 = 1000;
    }
    ch4 = 1500+(1500-ch4);
  }


  if (ch5 > 1800){
    if (servo[0].attached() && servo[1].attached()){
      servo[0].writeMicroseconds(ch2);
      servo[1].writeMicroseconds(ch4);
    } else{
      servo[0].attach(PA0,1000,2000,1500);
      servo[1].attach(PA1,1000,2000,1500);
    }
  } else{
    servo[0].detach();
    servo[1].detach();
  }

}


void setup()
{
    // Attach the channels callback
    crsf.onPacketChannels = &packetChannels;
}

void loop()
{
    // Must call CrsfSerial.loop() in loop() to process data
    crsf.loop();
    delay(20);
}
