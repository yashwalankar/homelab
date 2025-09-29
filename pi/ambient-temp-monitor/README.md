# Using SHT45 as Ambient Temp monitor

## Steps
### 1. Install Circuit Python using the UF2 file 
  - https://learn.adafruit.com/adafruit-sht4x-trinkey/install-circuitpython
### 2. Update code.py on the boot drive using `onboard/code.py`
* Testing   
   * Using MuEditor REPL on serial or  >> cat /dev/{PORT}
       * usually  `/dev/cu.usbmodem2101` on mac or `cat /dev/ttyACM0` on linux/pi

### 3 . Read through the serial port using python in Docker
