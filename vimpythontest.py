import imp
#
#au = imp.load_source('module.name', '/home/pi/spi_auguste/spi_can/can_lib_auguste.py')

import can_lib_auguste as au
imp.reload(au)

au.master_init()
au.getCurrent()
mean, std, pop = au.currentCal(100)
import RPi.GPIO as GPIO

au.getVoltageMaster()

au.getSlaveVoltage([0x03, 0x02, 0x01])
print("DONE")
au.getVoltage()
au.getRXBnSIDL()
int(au.getRXBnSIDL(), 2) & 0x80
au.getCANINTE()

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

au.master_exit()
