import network, time

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    time.sleep(5) # Required to prevent Thonny IDE from crashing
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
    time.sleep(5)
    return sta_if
    
    
def disconnect(interface):
    interface.active(False)