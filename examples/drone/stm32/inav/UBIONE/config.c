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

#include <stdbool.h>
#include <stdint.h>

#include <platform.h>

#include "drivers/serial.h"
#include "io/serial.h"
#include "fc/config.h"
#include "drivers/sound_beeper.h"
#include "drivers/pwm_output.h"

void targetConfiguration(void)
{
    beeperConfigMutable()->pwmMode = true;
    /*
     * Enable MSP at 115200 at UART4
     */
    serialConfigMutable()->portConfigs[findSerialPortIndexByIdentifier(SERIAL_PORT_USART2)].functionMask = FUNCTION_MSP;
    serialConfigMutable()->portConfigs[findSerialPortIndexByIdentifier(SERIAL_PORT_USART2)].msp_baudrateIndex = BAUD_115200;
}
