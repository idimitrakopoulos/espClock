from conf import config
from lib import ulogger
from lib import wifi
from hw import espled as led
from hw import tm1637, ssd1306
from machine import Pin, SPI
import ntptime, time, framebuf

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

# Turn off on-board led
led.turn_off()

# Initialize Screens
tm = tm1637.TM1637(clk=Pin(config.TM_CLK_PIN), dio=Pin(config.TM_DIO_PIN))
ssd = ssd1306.SSD1306_SPI(128, 64, SPI(2), Pin(16), Pin(17), Pin(5))
ssd.text('espClock (C)2022', 0, 0, 2)
ssd.show()

# buffer = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x10\x8a\n0\x10$\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\xfe\xff?\xfe\xfd|\xfb\xf8\xfc\xff|\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0@\xe0\xe0\xe0\xc0\xc1c\x9f\xff\x0f\xce\xff\xff\xcf\xe3\xf0pp\xa0\xe0\xe0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\xfb\xe7\xdf\x8e\x9e\xfd\x95"$%\x00\xfe\xff\xff\xed\xdd\xce\xce\xff\xe7\xe7\xf7\xfb\xf9\xfep\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@6\x9bg7\xcfo\x9d\xdb?\xbbws\xf7\xfa\xfa\xf9\xf4\xfd\xf7\xf3\xf1\xfdsy\xbd;\xd9\x9do\xcc6g\x9b6@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02\x01\x04\x03\t\x06\x13\x0c&\x19\r\x1b\x1b\r\x19&\x0c\x13\x06\t\x03\x04\x01\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# fb = framebuf.FrameBuffer(buffer, 48, 48, framebuf.MVLSB)
# ssd.fill(0)
# ssd.blit(fb, 8, 0, 0)
# ssd.show()

while True:
    # Convert to localtime
    localtime = time.localtime(time.time() + (int(config.UTC_OFFSET) * 60 * 60))

    # Fix brightness
    if config.LOW_BRIGHTNESS_HOUR_FROM <= localtime[3] <= config.LOW_BRIGHTNESS_HOUR_TO:
        tm.brightness(config.TM_LOW_BRIGHTNESS_SETTING)
        ssd.contrast(config.SSD_LOW_BRIGHTNESS_SETTING)
    else:
        tm.brightness(config.TM_HIGH_BRIGHTNESS_SETTING)
        ssd.contrast(config.SSD_HIGH_BRIGHTNESS_SETTING)
        
    tm.numbers(localtime[3], localtime[4])
