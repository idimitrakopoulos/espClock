import network, time

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    time.sleep(5)
    return sta_if
    
    
def disconnect(interface):
    interface.active(False)