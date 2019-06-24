# SCD30 Logger

CO2, Humidity and Temperature Logger using Sensirion SCD30 written in Python 3
for MicroPython. Continously logs date, time and sensor data on a file on the
SD card. The SD card as well as the sensor module is turned off to conserve
battery power (further improvements possible by using RTC wakeup instead of a
simple sleep).

## Getting Started

### Prerequisites

* Sensirion SCD30 Sensor
* Pyboard D (other MicroPython boards should work with some adjustments)

### Wiring

| Pyboard       | SCD30         |
| ------------- |---------------|
| X15 (3V3)     | VDD           |
| X14 (GND)     | GND           |
| X9            | TX/SCL        |
| X10           | RX/SDA        |

I recommend to also connect VBAT (Y15) to a backup battery. This makes sure that
the RTC keeps time when disconnecting the board and connecting it someplace
else.


### Installing

Copy main.py and lib/scd30.py on a SD-card and plug it into the board or
the internal flash (via USB).

The logger uses the RTC to write down when the measurement has been taken. Make
sure to set date and time correctly:

```python
from pyb import RTC
rtc = RTC()
rtc.datetime((2019, 6, 12, 3, 8, 49, 20, 0)) # y, m, d, weekday, h, m s, ms
rtc.datetime()
```

## Built With

* [MicroPython](http://micropython.org/)
* [SCD30](https://www.sensirion.com/en/environmental-sensors/carbon-dioxide-sensors-co2/)
- SCD30 Sensor Module (available from various suppliers)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details

