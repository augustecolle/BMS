import can_lib_auguste as au
import time

stime = 0.05

au.startSpi(500000, 1)
au.softReset()

au.setCANCTRL(0x80) #set configuration mode
au.setCANINTE(0x1F) #enable interrupts on transmit empty and on receive full
au.setCANINTF(0x00) #clear all interrupt flags
au.setRXBnCTRL(0x64)    #accept all incomming messages and enable roll over

au.setTXBnSIDH(0xFF, 0) #set standard identifier 8 high bits
au.setTXBnSIDL(0xFF, 0) #set low 3 bits stid and extended identifier
au.setTXBnEID8(0xFF, 0)
au.setTXBnEID0(0xFF, 0)

au.setCNF1(0x0F)
au.setCNF2(0x90)
au.setCNF3(0x02)

au.setTXBnDLC(0x08, 0)  #Transmitted message will be a dataframe with 8 bits
time.sleep(stime)
au.setTXBnDM([x*3 for x in range(8)], 0)
time.sleep(stime)

au.setCANCTRL(0x40) #set loopback mode
#
au.setTXBnCTRL(0x0B, 0) #set TXREQ bit high and highest message priority
time.sleep(stime)
#
#
print(au.getRXBnDM())   #print message if received

