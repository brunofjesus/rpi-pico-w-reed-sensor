import reed
import urequests as requests
from wlan import WLAN
from ups import UPS
import utime
import _thread
import lowpower
from machine import Pin #remove

use_internal_led = True
ssid = 'SSID'
password = 'PASSWD'
central = '192.168.1.100:8080'
device_name = 'garage_door'
debug = True

seconds_until_sleep = 20
last_action_count = seconds_until_sleep

def door_handler(is_open: bool):
    global last_action_count
    last_action_count = seconds_until_sleep
    
    if internal_led:
        internal_led.value(int(is_open))
    
    event = 'door_open' if is_open else 'door_closed'
    
    r = requests.post("http://{}/event/{}/{}".format(central,device_name,event))
    r.close()

def monitoring():
    global last_action_count
    
    while True:
        if last_action_count == 0:
            print("going to sleep")
            lowpower.dormant_until_pin(22)
            print("waking up")
            last_action_count = seconds_until_sleep
        else:
            last_action_count = last_action_count - 1
        print(last_action_count)
        utime.sleep(1)
    
def battery_reporter_thread(wifi):
    try:
        ups = UPS()
    except OSError:
        print("Cannot connect to UPS")
        return
    
    last_ups_pct = 0
    
    while True:
        stats = ups.stats()
        print(stats)

        if wifi.is_connected():            
            if stats['p'] != last_ups_pct:
                last_ups_pct = stats['p']
                r = requests.post("http://{}/event/{}/battery_{}".format(central,device_name,last_ups_pct))
                r.close()
        else:
            print("No connection")
            
        utime.sleep(60)

if __name__ == "__main__":
    # led
    internal_led = machine.Pin("LED", machine.Pin.OUT) if use_internal_led else None

    # start the wifi
    wifi = WLAN(ssid, password)
    wifi.connect()
    
    # start the sensor
    sensor = reed.ReedSensor(sensor_pin_id = 22, handler=door_handler)

    # monitor the UPS
    #_thread.start_new_thread(battery_reporter_thread, (wifi,))
    #monitoring()
    
    
 
