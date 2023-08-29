F411_TARGETS    += $(TARGET)
FEATURES        += VCP

TARGET_SRC = \
            drivers/barometer/barometer_dps310.c \
            drivers/accgyro/accgyro_spi_mpu6000.c \
            drivers/accgyro/accgyro_spi_icm20689.c \
            drivers/compass/compass_qmc5883l.c \
            $(ROOT)/lib/main/BoschSensortec/BMI270-Sensor-API/bmi270_maximum_fifo.c \
            drivers/accgyro/accgyro_spi_bmi270.c