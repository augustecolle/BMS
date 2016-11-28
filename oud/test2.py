import can_lib_auguste as au
import time

stime = 0.01

au.startSpi(5000000)
au.softReset()

au.setCANCTRL(0x80) #set configuration mode
au.setCANINTE(0x1F) #enable interrupts on transmit empty and on receive full
au.setCANINTF(0x00) #clear all interrupt flags
au.setRXBnCTRL(0x64)    #accept all incomming messages and enable roll over

au.setCANCTRL(0x00) #set normal mode
time.sleep(stime)

print(au.getRXBnDM())   #print message if received

