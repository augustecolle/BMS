import can_lib_auguste as au
import time
import RPi.GPIO as GPIO

au.master_init()
GPIO.output(25, GPIO.LOW)    
GPIO.output(25, GPIO.HIGH)    

stime = 0.05

au.startSpi(500000, 0)
au.startSpi(500000, 1)
au.softReset()
au.setBFPCTRL(0x0C)
au.getVoltageMaster()

au.setCANCTRL(0x80) #set configuration mode
au.setCANINTE(0x1F) #enable interrupts on transmit empty and on receive full
au.extendedID()        #enable extended identifier
au.setCANINTF(0x00) #clear all interrupt flags
au.setRXBnCTRL(0x64)    #accept all incomming messages and enable roll over
au.setCNF1(0x0F) # au.setCNF1(0xFF)    #Used to be:0x0F 
au.setCNF2(0x90) # au.setCNF2(0xA8)    #Used to be:0x90
au.setCNF3(0x02) # au.setCNF3(0x05)    #Used to be:0x02

au.setTXBnSIDH(0x00, 0) #set standard identifier 8 high bits
au.setTXBnSIDL(0x08, 0) #set low 3 bits stid and extended identifier
au.setTXBnEID8(0x00, 0)
au.setTXBnEID0(0x01, 0)

au.setTXBnDLC(0x08, 0)  #Transmitted message will be a dataframe with 8 bits
time.sleep(stime)
au.setTXBnDM([3 for x in range(8)], 0)
au.getTXBnDM()
time.sleep(stime)

au.setCANCTRL(0x40) #set loopback mode
au.setCANCTRL(0x00) #set normal mode
#

au.getCANINTF()
au.setCANINTF(0x00)
au.getCNF1()
au.setCANINTF(0x00)
au.getTXBnCTRL()
au.setTXBnCTRL(0x0B)
au.getEFLG()
au.getRXBnSIDL()
print(au.getVoltage())

au.setTXBnCTRL(0x0B, 0) #set TXREQ bit high and highest message priority
time.sleep(stime)
au.getCANINTF()

for x in range(100):
    au.getCurrent()


bat_dict = {1:[], 2:[], 3:[], 4:[], 5:[]}

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def update_plot(i, fig, scat):
    for x in range(4):
        au.setTXBnEID0((x % 4) + 5, 0)
        print(au.getTXBnEID0())
        au.setCANINTF(0x00)
        au.setTXBnCTRL(0x0B)
        print(au.getCANINTF())
        if ((x % 4) + 1 == 3):
            bat_dict[3].append(au.getVoltageMaster())
            GPIO.output(23, GPIO.LOW)    
            bat_dict[5].append(au.getCurrent())
            GPIO.output(23, GPIO.HIGH)
        else:
            volt = au.getVoltage()
            bat_dict[(x % 4) + 1].append(volt)
            time.sleep(0.10)
    print(np.array(bat_dict.values())[:,i])
    scat = plt.scatter([i]*5, np.array(bat_dict.values())[:,i])
    return scat,

plt.cla()

fig, ax = plt.subplots()
scat = plt.scatter([], [])

numframes = 100
numpoints = 5

color_data = np.random.random((numframes, numpoints))

ani = animation.FuncAnimation(fig, update_plot, fargs = (fig, scat), frames = numframes, interval=500)
plt.show()

print("DONE")

#
#
print(au.getRXBnDM())   #print message if received

