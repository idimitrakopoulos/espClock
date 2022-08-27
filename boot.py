from conf import config
from lib import ulogger
from lib import wifi
import ntptime, time

# Create Logger
handler_to_term = ulogger.Handler(
    level=ulogger.DEBUG,
    colorful=False,
    fmt="&(time)% - &(level)% - &(name)% - &(msg)%",
    clock=None,
    direction=ulogger.TO_TERM,
)
log = ulogger.Logger(
    name = __name__,
    handlers = (
        handler_to_term,
    )
)


log.info("espClock Project (C) 2022 -- Iason Dimitrakopoulos")

# Connect to WiFi
sta_if = wifi.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

# Get current time from NTP
ntptime.settime()

# Disconnect from WiFi
wifi.disconnect(sta_if)

from hw import tm1637
from machine import Pin
tm = tm1637.TM1637(clk=Pin(config.TM_CLK_PIN), dio=Pin(config.TM_DIO_PIN))

while True:
    # Convert to localtime
    localtime = time.localtime(time.time() + (int(config.UTC_OFFSET) * 60 * 60))
    
    # Fix brightness
    if config.LOW_BRIGHTNESS_HOUR_FROM <= localtime[3] <= config.LOW_BRIGHTNESS_HOUR_TO:
        tm.brightness(config.LOW_BRIGHTNESS_SETTING)
    else:
        tm.brightness(config.HIGH_BRIGHTNESS_SETTING)

    tm.numbers(localtime[3], localtime[4])
