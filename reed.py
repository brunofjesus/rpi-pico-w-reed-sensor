import machine
import utime


class ReedSensor():
    
    def __init__(self, sensor_pin_id, handler):
        self.reed = machine.Pin(sensor_pin_id, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.handler = handler
        
        self.is_open = self.reed.value() == 0
        if self.is_open:
            print("IS OPEN")
            self.reed.irq(trigger = machine.Pin.IRQ_RISING, handler=self.handle_closing)
        else:
            print("IS CLOSED")
            self.reed.irq(trigger = machine.Pin.IRQ_FALLING, handler=self.handle_opening)

    def handle_opening(self, pin):
        if not self.is_open:
            self.is_open = True
            self.reed.irq(trigger = machine.Pin.IRQ_RISING, handler=self.handle_closing)
            print("Door opened")
            if self.handler:
                self.handler(True)
            
        utime.sleep(1)

    def handle_closing(self, pin):        
        if self.is_open:
            self.is_open = False
            self.reed.irq(trigger = machine.Pin.IRQ_FALLING, handler=self.handle_opening)
            print("Door closed")
            if self.handler:
                self.handler(False)
            
        utime.sleep(1)



if __name__ == "__main__":
    internal_led = machine.Pin("LED", machine.Pin.OUT)
    
    def handler(is_open: bool):
        internal_led.value(int(is_open))
        
    rs = ReedSensor(sensor_pin_id = 22, handler=handler)