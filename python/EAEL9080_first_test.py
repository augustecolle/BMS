import EAEL9080 as au
import numpy as np
import math
import time as tm
import csv

au.startSerial('/dev/ttyUSB1', "02")
au.setRemoteControllOn()

logtime = 1 #seconds
numlines = 1000 #lines in each csv file

cyclelog = 0
naamt = 0
listOfVolts = []
listOfCurrents = []
listOfTimestamps = []

au.setInputOn()
au.setCCMode()
au.setCurrentA(30) #
au.setVoltageA(17)
au.setPowerA(1000)
au.clearBuffer()

while(au.getActualValues()[0] > (2.85*4)):
    start = tm.time()
    cyclelog += 1
    temp = au.getActualValues()
    print("Discharging cycle log: " + str(cyclelog))
    print("[Voltage, Current, Power]: " + str(temp))
    listOfVolts.append(temp[0])
    listOfCurrents.append(temp[1])
    listOfTimestamps.append(tm.strftime("%H:%M:%S", tm.localtime()))
    if (cyclelog > numlines):
        listname = 'test__discharge2_'+str(naamt).zfill(4)+'.csv'
        naamt += 1
        cyclelog = 0
        header = ['Tijd', 'Spanning', 'Stroom']
        list = zip(listOfTimestamps, listOfVolts, listOfCurrents)
        with open(listname, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(header)
            writer.writerows(list)
        listOfVolts = []
        listOfCurrents = []
        listOfTimestamps = []
    #wait till one second passed since beginning of cycle
    tm.sleep(logtime - (tm.time() - start))

listname = 'test_discharge2_'+str(naamt).zfill(4)+'.csv'
header = ['Tijd', 'Spanning', 'Stroom']
list = zip(listOfTimestamps, listOfVolts, listOfCurrents)

with open(listname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(header)
    writer.writerows(list)

au.setCurrentA(0)
au.setVoltageA(0)
au.setPowerA(0)
au.setInputOff()
au.setRemoteControllOff()
au.stopSerial()
