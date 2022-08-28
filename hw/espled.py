from machine import Pin


def turn_on():
    led = Pin(2, Pin.OUT)
    led.on()
    
def turn_off():
    led = Pin(2, Pin.OUT)
    led.off()

