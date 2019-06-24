from pyb import LED
import sys, os, pyb
import machine
from machine import Pin
import time
import utime
from scd30 import SCD30
from machine import I2C

errled = LED(1)
led = LED(2)

# Get Sensor, should be scannable here...
i2c = I2C(1)
scd30 = SCD30(i2c, 0x61)

# Make sure we have a SD card!
sd = pyb.SDCard()

if sd.present() != 1:
    errled.on()
    machine.deepsleep()

# Power off the board...
sd.power(0)

en_3v3 = Pin('EN_3V3')
en_3v3.value(0)


while True:
    data = { }
    en_3v3.value(1)
    led.on()

    sd.power(1)
    os.mount(pyb.SDCard(), '/sd')

    # Get local time when taking measurement
    for i in range(30):
        t = utime.localtime()

        while scd30.get_status_ready()[0] != 1:
            time.sleep_ms(200)
        time.sleep_ms(200)
        try:
            measurement = scd30.read_measurement()
            data['co2'] = measurement[0][0]
            data['temperature'] = measurement[1][0]
            data['humidity'] = measurement[2][0]
            print('co2: {}, temperature: {}, humidity: {}'.format(data['co2'], data['temperature'],
                data['humidity']))
        except SCD30.CRCException:
            print('CRC exception during measurement reading SCD30')
            errled.on()
            pass

        # Create logfile per day...
        datetimeformat = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'
        isodatetime = datetimeformat.format(t[0], t[1], t[2], t[3], t[4], t[5])
        name = 'sensordata_{:04d}_{:02d}_{:02d}.log'.format(t[0], t[1], t[2])

        with open("/sd/" + name, "a") as f:
            f.write("{};{};{};{};\n".format(isodatetime, data['co2'], data['temperature'], data['humidity']))


    os.umount('/sd')
    sd.power(0)
    en_3v3.value(0)
    led.off()

    # Sleep for 300 seconds...
    time.sleep(300)

