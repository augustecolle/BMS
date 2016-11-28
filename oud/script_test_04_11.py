import can_lib_auguste as au
import RPi.GPIO as GPIO

au.startSpi(1)
GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)

au.getCANCTRL()
au.setBFPCTRL(0x1C)
