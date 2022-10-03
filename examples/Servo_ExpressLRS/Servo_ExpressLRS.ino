#include <CrsfSerial.h>
#include <Servo.h>

HardwareSerial Modem(USART1);

Servo servo[1];

CrsfSerial crsf(Modem, CRSF_BAUDRATE); // pass any HardwareSerial port

/***
 * This callback is called whenever new channel values are available.
 * Use crsf.getChannel(x) to get us channel values (1-16).
 ***/
void packetChannels()
{
    Serial.print("CH1=");
    Serial.println(crsf.getChannel(1));

    servo[0].writeMicroseconds(crsf.getChannel(1));
}


void setup()
{
    Serial.begin(115200);

    // If something other than changing the baud of the UART needs to be done, do it here
    // Serial1.end(); Serial1.begin(500000, SERIAL_8N1, 16, 17);

    // Attach the channels callback
    crsf.onPacketChannels = &packetChannels;
  servo[0].attach(PA0,1000,2000,1500);

    
}

void loop()
{
    // Must call CrsfSerial.loop() in loop() to process data
    crsf.loop();
}
