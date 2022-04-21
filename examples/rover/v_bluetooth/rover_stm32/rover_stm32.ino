#include <Servo.h>
#define DEBUG Serial

//HardwareSerial DEBUG(USART2); //A2(TX) and A3(RX)
HardwareSerial RPI(USART2);

const byte MAX_REC_BYTES = 12;      // Maximum received bytes allowed
int receiveBuffer[MAX_REC_BYTES];
bool serialRead = true;
int maxWithoutSerial = 200;
unsigned long lastSerial = 0;
const byte NMOTORS = 2;
unsigned long blink_timer = millis();


Servo servo[NMOTORS]; // 1 for the main DC motor, 1 for the left right servo and 2 for the camera gimbal

void setup() {

  /* Begin serial communication for remote control */
  DEBUG.begin(115200);                                          //Set the serial output to 57600 kbps.
  RPI.begin(115200);
  pinMode(PC13, OUTPUT);
  DEBUG.println("Ready");

}

void loop() {

  int currentMillis = millis();
  if (currentMillis - lastSerial >= maxWithoutSerial){
    for (int i = 0;i < NMOTORS;i++){
      if (servo[i].attached()){
        servo[i].writeMicroseconds(1500);
      }
    }
  }
  /* Receive the remote controller's commands */
  if (RPI.available() >= MAX_REC_BYTES && serialRead){
    receiveControl();
  }
  blinkLED();

  delay(10);
}

/**
 * LLED blink to make sure the main loop is running and not stuck
 */
void blinkLED() {
  if(millis()-blink_timer > 1000) {
    int level = digitalRead(PC13);
    digitalWrite(PC13, !level);
    blink_timer = millis();
    DEBUG.println("DEBUG OK");
  }
}

void receiveControl() {
  serialRead = false;

  int i = 0;
  for (int i=0;i<MAX_REC_BYTES;i++){
    receiveBuffer[i] = RPI.read();
  }
  while(RPI.available()){
    RPI.read();
  }

 for(i = 0;i<NMOTORS+1;i++){
  int pos = i;
  int cmds = receiveBuffer[i*4];
  int pin = receiveBuffer[i*4+1];
  int hsb = receiveBuffer[i*4+2];
  int lsb = receiveBuffer[i*4+3];
  int ms = hsb*256 + lsb;

  DEBUG.print(pos);
  DEBUG.print(" |" );
  DEBUG.print(cmds);
  DEBUG.print(" |" );
  DEBUG.print(pin);
  DEBUG.print(" |" );
  DEBUG.print(hsb);
  DEBUG.print(" |" );
  DEBUG.print(lsb);
  DEBUG.print(" |" );
  DEBUG.println(ms);



  switch (cmds) {
    case 10:
      servo[pos].attach(pin,1000,2000,1500);
      break;
    case 15:
      servo[pos].writeMicroseconds(ms);
      break;
    case 20:
      servo[pos].detach();
      break;
    case 30:
      tone(pin, ms, 100);
      break;
    default:
      break;
  }

 }
 lastSerial = millis();
 serialRead = true;
}
