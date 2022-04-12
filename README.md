# UbiOne


* [Introduction](https://github.com/Ubiqu0/UbiOne/#introduction)<br>
* [Upload sketchs](https://github.com/Ubiqu0/UbiOne/#upload-sketchs)<br>
  * [DFU](https://github.com/Ubiqu0/UbiOne/#dfu)<br>
  * [SWD](https://github.com/Ubiqu0/UbiOne/#swd)<br>
  * [Serial](https://github.com/Ubiqu0/UbiOne/#serial)<br>
* [Pinout](https://github.com/Ubiqu0/UbiOne/#pinout)<br>
  * [RPI](https://github.com/Ubiqu0/UbiOne/#rpi)<br>
  * [mPCIe](https://github.com/Ubiqu0/UbiOne/#mpcie)<br>
  * [I2S Microphone](https://github.com/Ubiqu0/UbiOne/#i2s-microphone)<br>
  * [Buzzer](https://github.com/Ubiqu0/UbiOne/#buzzer)<br>
  * [IMU and Pressure sensor](https://github.com/Ubiqu0/UbiOne/#imu-and-pressure-sensor)<br>


# Introduction

**UbiOne** is a Raspberry Pi HAT that combines an **STM32F411**, a set of **sensors**, and a **Mini-PCIe socket** to provide **LTE** connectivity to your RPI.

It includes an IMU (**ICM-20689**), a pressure sensor (**SPL06-001** that is equivalent to DPS310 sensor), an I2S microphone (**SPH0645**), and a small passive buzzer (**KLJ-4020**).

Furthermore, it manages the RPI power supply, which means you can completely shutdown the RPI and have a **true long-term sleep mode**.

**UbiOne** was designed having in mind the use of [ubiquo.net](https://ubiquo.net), a web application that allows you to control your DIY bot remotely via web browser (currently as a demo only).


![UbiOne_v.9.3](https://github.com/Ubiqu0/UbiOne/blob/main/hardware/UbiOne_board_table_v0.9.3.png)

**IMPORTANT:** **UbiOne** is not yet in production! I have a working tested **prototype**, and I plan to start crowdfunding (e.g., Indiegogo) to fund the production. If you are interested, please fill out this [form](https://forms.gle/ZSxchesgbg77n8198) with your contact, and I will notify you about the campaign.  


UbiOne  | UbiOne + RPI  | UbiOne + LTE + RPI + Camera |    
:------:|:------------: |:---------------------------: |
![](https://github.com/Ubiqu0/UbiOne/blob/main/hardware/ubione.png) | ![](https://github.com/Ubiqu0/UbiOne/blob/main/hardware/ubione_rpi.png) | ![](https://github.com/Ubiqu0/UbiOne/blob/main/hardware/ubione_lte_rpi_camera.png) |


------

# Geting Started

You can use Arduino IDE to program and upload sketchs using [Arduino Core for STM32](https://github.com/stm32duino/Arduino_Core_STM32). You can follow these [steps](https://github.com/stm32duino/wiki/wiki/Getting-Started) to install the STM32 libraries or, very shortly:

- Open Arduino "**Preferences**" and add the following link to "**Additional Boards Manager URLs**":
```
https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json
```
1. Go to "**Tools > Board > Board Manager**" and search for "**STM32**"
2. Install the package "**STM32 MCU based boards**"
3. Install [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)

Select the STM32 board type and respective configuration:

1. Go to "**Tools > Board > STM32 Boards groups > Generic STM32F4 series**"
2. Select the board part number "**Tools > Board > Board part number**" and select "**Generic F411CEUx**"
3. Enable serial to be able to print to the Serial Monitor: "**Tools > U(S)ART support: Enabled (generical 'Serial')**"
4. Enable "**USB support (if available): CDC (generical 'Serial'...)**"

In the end, you should have the following configuration:


<img width="515" alt="Screenshot 2022-04-09 at 12 48 33" src="https://user-images.githubusercontent.com/7373193/162572820-2bcd1df8-db56-4324-b21e-a6e2f1499c62.png">



------

# Upload sketchs

You can upload sketches from three different ways: **DFU**, **SWD**, or **Serial**.

## DFU

To compile and upload in **DFU mode** go to "**Tools > Upload method > STM32CubeProgrammer (DFU)**".

Now, follow the next steps:

  1. Connect your PC to **UbiOne** through the <ins>STM32 USB-C port</ins>.
  2. Put the STM32 MCU in **programming mode** by:
      1. pressing and holding **BOOT**
      2. press and release **NRST**
      3. release **BOOT**
  3. Arduino IDE is now ready to compile and upload (click upload in Arduino IDE)

## SWD

To compile and upload in **SWD mode** go to "**Tools > Upload method > STM32CubeProgrammer (SWD)**". To program via SWD you need an ST-LINK/V2, that can be the [official](https://www.st.com/content/st_com/en/products/development-tools/hardware-development-tools/hardware-development-tools-for-stm32/st-link-v2.html) or a smaller (and cheaper) version like this one:

![Screen Shot 2021-11-24 at 11 11 21](https://user-images.githubusercontent.com/7373193/143227929-663da6c6-d013-44a5-9de1-07ea58ddc182.png)


When uploading via SWD, you don't need to put the STM32 in any particular mode. All you need is to connect the pins:

  - **GND**
  - **SWDIO**
  - **SWCLK**
  - **3.3V** (optional: you should connect only in case you are powering the UbiOne through the ST-LINK/V2)


## Serial

A third option is to program through Serial, using, for example, an FTDI USB UART converter like this one:

![Screen Shot 2021-11-24 at 17 13 34](https://user-images.githubusercontent.com/7373193/143284618-a39b0a6f-5fe8-471d-96d9-1667574d1b42.png)


To compile and upload in **UART mode** go to "**Tools > Upload method > STM32CubeProgrammer (Serial)**". 

Next, follow the steps:
  1. Connect the pins:
     1. RX to A9
     2. TX to A10
     3. GND to GND
     4. 3.3V to 3.3V or 5V to 5V (it depends on the option you have selected in the FTDI converter).
  2. Put the STM32 MCU in **programming mode** by
      1. pressing and holding **BOOT**
      2. press and release **NRST**
      3. release **BOOT**
  3 Arduino IDE is now ready to compile and upload (click upload in Arduino IDE)

---
# Pinout

The following pins are available through the pin headers: **PB7, PB6, PA4, PA5, PA10, PA9, PA0, PA1, PA6, PA7, PB0, PB10, B13, PB15, and PB1**. You can find more details about each in the [datasheet](https://www.st.com/en/microcontrollers-microprocessors/stm32f411ce.html). You can also use [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) (search for STM32F411CEU).


## RPI

UbiOne can be interfaced with the 40-pin RPI header.

| STM32 |  RPI GPIO | RPI Pin | Function | 
| :-----: | :-----: |  :-----: | :-----: |
| PB9  | GPIO2 (SJ1) | 3 | I2C_SDA | 
| PB8  | GPIO3 (SJ2) | 5 | I2C_SCL | 
| PA3  | GPIO14  | 8 | UART2_RX |
| PA2  | GPIO15  | 10 | UART2_TX |


SJ* means a solder jumper.  By default, they are not connected, and therefore you need to solder it in case of use.

As the table shows, **UbiOne** can communicate directly with the RPI via UART pins (GPIO14 and GPIO15). Please note that to do so, you need to first to configure the RPI:

1. Go to the RPI system configuration menu by typing ```sudo raspi-config``` in a terminal.
2. Go to "**Interface Options > Serial Port**"
3. Select "**No**" to the first question (related to login)
4. Select "**Yes**" to the second question to enable serial

## mPCIe

**UbiOne** can fit a Mini-PCIe card based on the pinout of a [Quectel LTE EC25 Mini PCIe](https://www.quectel.com/product/lte-ec25-mini-pcie-series). In case you use any other card, you should pay attention if it respects the same pin configuration.

| STM32 |  mPCIe function | mPCIe pin |
| :-----: | :-----: |  :-----: |
| PA10 | TX | 13 |
| PA9  | RX | 11 |
| PA8 | RI | 17 |
| PA15 | DTR | 31 |
| PA4 (SJ3) | WAKE | 1 |
| PA5 (SJ4) | W_DISABLE | 20 |

If you need to use WAKE and W_DISABLE functions you must solder **SJ3** and **SJ4**.

## I2S Microphone

**UbiOne** incorporates an I2S microphone. The setup is the same as the [I2S MEM Microphone board from Adafruit](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/overview), where the mic is directly connected to RPI through GPIO pins GPIO18, GPIO19, and GPIO20. To use with the RPI just follow the [Adafruit guide](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test).

**NOTE**: for some reason, the file `~/.asoundrc` keeps getting deleted (related to [this](https://forums.raspberrypi.com/viewtopic.php?t=295008) issue). So if you notice any problem with the microphone, please first check if the file is there.

| RPI |  Microphone | 
| :-----: | :-----: | 
| GPIO18 | BCLK |  
| GPIO19  | WS | 
| GPIO20 | DATA |

## Buzzer

Since **UbiOne** has a microphone, it would be nice to have a speaker. However, we think we can agree it would be pretty challenging to add a speaker to this little board. Even so, we added a small buzzer to pin **PB14** that allows playing a simple buzz and some nice tunes.  Try, for example, [this](https://github.com/Ubiqu0/UbiOne/blob/main/examples/buzzer/very_nice_tune.ino) one! :wink:

## IMU 

The IMU sensor (ICM-20689) is by default connected to the STM32F411 through an SPI connection:

| IMU |  STM32 | 
| :-----: | :-----: | 
| MISO | PB4 |  
| MOSI | PB5 |  
| SCK  | PB3 | 
| CS | PB12 |
| INT | PC14 |


If you want to use I2C instead, you must solder **SJ5**, **SJ6** and **SJ7**. You should also remove resistors **R38** and **R39** to release SCK and MOSI connections from the STM32F411. In this scenario we have the following connections:

| IMU |  STM32 | 
| :-----: | :-----: | 
| SDA | PB9 |  
| SCL | PB8 |  


You can also  make readings from the RPI using its I2C port. For such scenario you must use RPI I2C pins **GPIO2** and **GPIO3**, and solder **SJ1**, **SJ2**. If you ask why it isn't everything connected, the RPI can only behave as master and does not support I2C multi-master. When connected, you lose the possibility of using the STM32 as a master in an I2C communication.

## Pressure sensor

The pressure sensor (SPL06-001) is permantly connected through a I2C connection. Again, if you want to read from the RPI you must solder **SJ1**, **SJ2**.

| SPL06 |  STM32 | 
| :-----: | :-----: | 
| SDA | PB9 |  
| SCL | PB8 |  
