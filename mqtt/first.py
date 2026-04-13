import utime
import machine
led = machine.Pin("LED", machine.Pin.OUT)

while True:
    led.off()
    utime.sleep(1)
    led.on()
    utime.sleep(1)