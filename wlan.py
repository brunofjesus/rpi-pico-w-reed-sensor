import time
import network

class WLAN():
    
    def __init__(self, ssid :str, password: str):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        
    def active(self, enable :bool):
        self.wlan.active(enable)
    
    def is_active(self):
        return self.wlan.active()
    
    def ifconfig(self):
        return self.wlan.ifconfig()
    
    def is_connected(self):
        return self.wlan.isconnected()
        
    def connect(self):
        self.active(True)
        self.wlan.connect(self.ssid, self.password)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        # Handle connection error
        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print( 'ip = ' + status[0] )

