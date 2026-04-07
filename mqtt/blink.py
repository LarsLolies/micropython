from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
for i in range(10):
    pin.toggle()
    sleep(1) # sleep 1sec


pin.off()
print("Finished.")
