import imp
#
#au = imp.load_source('module.name', '/home/pi/spi_auguste/spi_can/can_lib_auguste.py')

import can_lib_auguste as au
import RPi.GPIO as GPIO
imp.reload(au)

au.startSpi(1000, 0)
au.startSpi(1000, 1)

GPIO.output(25, GPIO.LOW)    
GPIO.output(25, GPIO.HIGH)    
GPIO.output(23, GPIO.HIGH)    
GPIO.output(23, GPIO.LOW)    

GPIO.output(26, GPIO.HIGH)    
GPIO.output(21, GPIO.HIGH)
GPIO.output(20, GPIO.HIGH)    

au.getBFPCTRL()
au.setBFPCTRL(0x2C)
au.setBFPCTRL(0x3C)
au.setBFPCTRL(0x1C)
au.getVoltage()
au.getData()
au.setBFPCTRL(0x3C)

au.getCurrent()
print("DONE")
a = time.time()
mean, std, pop = au.currentCal(100)
b = time.time()
print(b-a)
au.getVoltageMaster()

CNF1 = 0x0F 
CNF2 = 0x90
CNF3 = 0x02
au.getCANCTRL()
au.softReset()
au.setCANCTRL(0x80) #set configuration mode
au.setCANINTE(0x0E) #enable interrupts on transmit empty and on receive full
au.extendedID()        #enable extended identifier
au.setCANINTF(0x00) #clear all interrupt flags
au.setRXBnCTRL(0x64)    #accept all incomming messages and enable roll over
au.setCNF1(CNF1)    #Used to be:0x0F 
au.setCNF2(CNF2)    #Used to be:0x90
au.setCNF3(CNF3)    #Used to be:0x02

au.setTXBnSIDH(0x00, 0) #set standard identifier 8 high bits
au.setTXBnSIDL(0x08, 0) #set low 3 bits stid and extended identifier
au.setTXBnEID8(0x00, 0)
au.setTXBnEID0(0x01, 0)

au.setTXBnDLC(0x01, 0)  #Transmitted message will be a dataframe with 1 bits
au.setTXBnDM([3 for x in range(8)], 0)
au.setCANCTRL(0x00)

au.getTXBnDM()

au.getCANINTF()
au.setCANINTF(0x00)
au.getTXBnCTRL()
au.setTXBnCTRL(0x0B)
au.setTXBnCTRL(0x00)
au.getVoltage()
print(au.getVoltage())

au.setEFLG(0x00)
au.setTXBnCTRL(0x00)
au.getTEC()
au.getREC()
au.getEFLG()

#-------------CALIBRATION DAY CMON--------------------

import time
import numpy as np

num_loops = 10
res_list = []
c_time = 0

for x in range(num_loops):
    c_time = time.time()
    au.setCANINTF(0x00)
    au.setTXBnCTRL(0x0B)
    volt = au.getVoltage()
    res_list.append(volt)
    while (time.time() < c_time + 1):
        pass

with open("dead_cell_performance", "w") as text_file:
    for x in range(num_loops):
        text_file.write("%.8f\n" %(res_list[x]))
print("DONE")



#--------------RUN TEST CAN PERFORMANCE------------------------

import time
import numpy as np

num_loops = 10
TEClist = []
REClist = []
voltage = []
for x in range(num_loops):
    au.setCANINTF(0x00)
    au.setTXBnCTRL(0x08)
    while (int(au.getCANINTF()) & 0x01 != 1):
        time.sleep(0.1)
        print("waiting...")
    TEClist.append(int(au.getTEC(), 2))
    REClist.append(int(au.getREC(), 2))
    voltage.append(au.getVoltage())
with open("%s, %s, %s.txt" %(hex(CNF1), hex(CNF2), hex(CNF3)), "w") as text_file:
    text_file.write("TEC, REC, voltage\n")
    for x in range(num_loops):
        text_file.write("%d, %d, %.6f\n" %(TEClist[x], REClist[x], voltage[x]))
    text_file.write("mean: %.4f, %.4f" %(np.mean(TEClist), np.mean(REClist)))
print("DONE")

#----------------------------END------------------------------


print(TEClist)
print(REClist)
print(voltage)

