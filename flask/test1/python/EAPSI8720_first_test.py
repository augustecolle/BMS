import EAPSI8720 as au
import math
import csv
import numpy as np
import time as tm


au.startSerial()
au.remoteControllOn()
au.readAndTreat()

logtime = 1 #seconds
numlines = 1000 #lines in each csv file

cyclelog = 0
naamt = 0
listOfVolts = []
listOfCurrents = []
listOfTimestamps = []

#Charge at  bulck charge untill battery voltage is 42V
au.setCurrent(15)
au.setVoltage(16.1)
au.setPower(400)
while(au.getActualValues()[0] < 16.0):
    start = tm.time()
    cyclelog += 1
    print("bulk charging, cyclelog: " + str(cyclelog))
    temp = au.getActualValues()
    listOfVolts.append(temp[0])
    listOfCurrents.append(temp[1])
    listOfTimestamps.append(tm.strftime("%H:%M:%S", tm.localtime()))
    if (cyclelog > numlines):
        listname = 'test_charge'+str(naamt).zfill(4)+'.csv'
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
        

#Absorption fase, charge at 16 untill current < 55mA*5
begin = tm.time()
au.setVoltage(16.0)
while(au.getActualValues()[1] > (0.055*5)):
    start = tm.time()
    cyclelog += 1
    print("Absorption charging, cyclelog: " + str(cyclelog))
    temp = au.getActualValues()
    listOfVolts.append(temp[0])
    listOfCurrents.append(temp[1])
    listOfTimestamps.append(tm.strftime("%H:%M:%S", tm.localtime()))
    if (cyclelog > numlines):
        listname = 'test_charge'+str(naamt).zfill(4)+'.csv'
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

listname = 'test_charge'+str(naamt).zfill(4)+'.csv'
naamt += 1
cyclelog = 0
header = ['Tijd', 'Spanning', 'Stroom']
list = zip(listOfTimestamps, listOfVolts, listOfCurrents)
with open(listname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(header)
    writer.writerows(list)

au.setVoltage(0)
au.setCurrent(0)
au.stopSerial()
