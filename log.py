import can_lib_auguste as au
import time

runtime = 60*60         #in seconds
loginterval = 1         #in seconds

stime = 0.05

au.startSpi(500000, 1)
au.softReset()

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
au.setTXBnEID0(0x04, 0)

au.setTXBnDLC(0x08, 0)  #Transmitted message will be a dataframe with 8 bits
time.sleep(stime)
au.setTXBnDM([3 for x in range(8)], 0)
au.getTXBnDM()
time.sleep(stime)
au.getCANINTF()
au.setCANINTF(0x00)

au.setCANCTRL(0x40) #set loopback mode
au.setCANCTRL(0x00) #set normal mode
#
bat_dict = {1:[], 2:[], 3:[], 4:[]}

start = time.time()

while (time.time() - start < runtime):
    begin=time.time()
    for x in range(4):
        au.setTXBnEID0((x % 4) + 1, 0)
        #print(au.getTXBnEID0())
        au.setCANINTF(0x00)
        au.setTXBnCTRL(0x0B)
        time.sleep(0.10)
        volt = au.getVoltage()
        au.setCANINTF(0x00)
        bat_dict[(x % 4) + 1].append(volt)
        print(time.time() - start)
    while(time.time() - begin < loginterval):
        pass

print(volt)

print("DONE")



