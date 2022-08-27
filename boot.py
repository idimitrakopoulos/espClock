import tm1637, time
from machine import Pin
tm = tm1637.TM1637(clk=Pin(2), dio=Pin(4))

if time.gmtime()[3] <= 0 <= 24:
    tm.brightness(val=1)
else:
    tm.brightness(val=5)


tm.numbers(time.gmtime()[3], time.gmtime()[4])
