/*
 * This file is part of Cleanflight and Betaflight.
 *
 * Cleanflight and Betaflight are free software. You can redistribute
 * this software and/or modify this software under the terms of the
 * GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version.
 *
 * Cleanflight and Betaflight are distributed in the hope that they
 * will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software.
 *
 * If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#define USE_TARGET_CONFIG

#define TARGET_BOARD_IDENTIFIER "UB1"
#define USBD_PRODUCT_STRING     "UBIONE"

#define LED0_PIN                PC13

#define USE_BEEPER
#define BEEPER_PIN              PB13
#define BEEPER_INVERTED
#define BEEPER_PWM_HZ             2000 // Beeper PWM frequency in Hz

// *************** Gyro & ACC **********************
#define USE_SPI
#define USE_SPI_DEVICE_3
#define SPI3_SCK_PIN               PB3
#define SPI3_MISO_PIN              PB4
#define SPI3_MOSI_PIN              PB5
#define SPI3_NSS_PIN            PB12

#define GYRO_1_SPI_INSTANCE    SPI3
#define GYRO_1_CS_PIN          SPI3_NSS_PIN
#define GYRO_1_ALIGN      CW0_DEG

#define USE_EXTI
#define USE_GYRO_EXTI
#define GYRO_1_EXTI_PIN         PC14
#define USE_MPU_DATA_READY_SIGNAL
#define ENSURE_MPU_DATA_READY_IS_LOW


#define USE_GYRO
#define USE_GYRO_SPI_MPU6000
#define USE_GYRO_SPI_ICM20689

#define USE_ACC
#define USE_ACC_SPI_MPU6000
#define USE_ACC_SPI_ICM20689
#define USE_ACCGYRO_BMI270

// *************** Baro and Mag **************************
#define USE_I2C

#define USE_I2C_DEVICE_1
#define I2C_DEVICE              (I2CDEV_1)
#define I2C1_SCL                PB8        // SCL pad
#define I2C1_SDA                PB9        // SDA pad
#define BARO_I2C_INSTANCE       (I2CDEV_1)

#define USE_BARO                          //External, connect to I2C1
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

#define SERIAL_PORT_COUNT       3 //VCP, USART1, USART2


// *************** OSD/FLASH *****************************

// *************** ADC *****************************


#define USE_ADC
#define ADC_INSTANCE         ADC1  // Default added
#define ADC1_DMA_OPT            0  // DMA 2 Stream 0 Channel 0 
#define VBAT_ADC_PIN            PB1
#define DEFAULT_VOLTAGE_METER_SOURCE    VOLTAGE_METER_ADC

// *************** RPI PWR *****************************

#define USE_PINIO
#define PINIO1_PIN              PC15 // RPI EN
#define USE_PINIOBOX

#define TARGET_IO_PORTA 0xffff
#define TARGET_IO_PORTB 0xffff
#define TARGET_IO_PORTC 0xffff
#define TARGET_IO_PORTD 0xffff
#define TARGET_IO_PORTE 0xffff

#define USABLE_TIMER_CHANNEL_COUNT 7
#define USED_TIMERS             ( TIM_N(1)|TIM_N(2)|TIM_N(3)|TIM_N(4)|TIM_N(5)|TIM_N(9) )