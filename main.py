import reed
import urequests as requests
import wlan

use_internal_led = True
ssid = 'NSA'
password = '0d34c2f565'
central = '192.168.1.85:8080'
device_name = 'garage_door'

if __name__ == "__main__":
    internal_led = machine.Pin("LED", machine.Pin.OUT) if use_internal_led else None
    
    wlan.connect(ssid, password)
    
    def handler(is_open: bool):
        if internal_led:
            internal_led.value(int(is_open))
        
        event = 'door_open' if is_open else 'door_closed'
            
        r = requests.post("http://{}/event/{}/{}".format(central,device_name,event))
        r.close() # prevent mem leak
        
    sensor = reed.ReedSensor(sensor_pin_id = 22, handler=handler)