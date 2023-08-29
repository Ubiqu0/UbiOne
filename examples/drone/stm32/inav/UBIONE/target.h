/*
 * This file is part of Cleanflight.
 *
 * Cleanflight is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Cleanflight is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Cleanflight.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#define TARGET_BOARD_IDENTIFIER "UB1"
#define USBD_PRODUCT_STRING     "UBIONE"

//#define HSE_MZ 25

USE_GPS
USE_GPS_PROTO_UBLOX
USE_GPS_PROTO_NMEA
USE_GPS_PROTO_MSP

#define LED0                    PC13

#define BEEPER                  PB13
#define BEEPER_INVERTED
#define BEEPER_PWM_HZ             2000

// *************** SPI **********************

#define USE_SPI
#define USE_SPI_DEVICE_3
#define SPI3_SCK_PIN               PB3
#define SPI3_MISO_PIN   	   PB4
#define SPI3_MOSI_PIN   	   PB5
#define SPI3_NSS_PIN            PB12

#define GYRO_1_SPI_INSTANCE    SPI3
#define GYRO_1_CS_PIN          SPI3_NSS_PIN
#define GYRO_1_ALIGN      CW0_DEG

#define USE_EXTI
#define USE_GYRO_EXTI
#define GYRO_1_EXTI_PIN         PC14
#define USE_MPU_DATA_READY_SIGNAL
#define ENSURE_MPU_DATA_READY_IS_LOW


#define USE_IMU_BMI270
#define BMI270_CS_PIN         SPI3_NSS_PIN
#define BMI270_SPI_BUS        BUS_SPI3
#define IMU_BMI270_ALIGN      CW0_DEG

// *************** Baro & Mag *****************************

#define USE_I2C
#define USE_I2C_DEVICE_1
#define I2C1_SCL                PB8
#define I2C1_SDA                PB9

#define USE_BARO
#define BARO_I2C_BUS		    BUS_I2C1
#define USE_BARO_DPS310

#define USE_MAG
#define MAG_I2C_BUS             BUS_I2C1
#define USE_MAG_QMC5883


// *************** UART *****************************

#define USE_VCP

#define USE_UART1
#define UART1_TX_PIN            PA9
#define UART1_RX_PIN            PA10

#define USE_UART2
#define UART2_RX_PIN            PA3
#define UART2_TX_PIN            PA2

#define USE_SOFTSERIAL1
#define SOFTSERIAL_1_TX_PIN     PB6
#define SOFTSERIAL_1_RX_PIN     PB7

#define USE_SOFTSERIAL2
#define SOFTSERIAL_2_TX_PIN     PA8
#define SOFTSERIAL_2_RX_PIN     PA15


#define DEFAULT_RX_TYPE         RX_TYPE_SERIAL
#define SERIALRX_PROVIDER       SERIALRX_SBUS
#define SERIALRX_UART           SERIAL_PORT_USART1

#define SERIAL_PORT_COUNT       5       // VCP, USART1,USART2,SS1,SS2

// *************** ADC *****************************

#define USE_ADC
#define ADC_INSTANCE                    ADC1
#define ADC_CHANNEL_1_PIN               PB1
#define VBAT_ADC_CHANNEL                ADC_CHN_1

// *************** RPI PWR ***************************
#define USE_PINIO
#define USE_PINIOBOX
#define PINIO1_PIN                  PC15 // RPI EN

// ***************  OTHERS *************************
#define DEFAULT_FEATURES                ( FEATURE_VBAT | FEATURE_SOFTSERIAL)

#define USE_DSHOT

#define TARGET_IO_PORTA         0xffff
#define TARGET_IO_PORTB         0xffff
#define TARGET_IO_PORTC         0xffff
#define TARGET_IO_PORTD        (BIT(2))

#define MAX_PWM_OUTPUT_PORTS       6