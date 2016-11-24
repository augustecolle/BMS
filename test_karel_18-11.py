import imp

au = imp.load_source('module.name', '/home/pi/spi_auguste/spi_can/can_lib_auguste.py')

au.startSpi(500000, 0)

CNF1 = 0x0F 
CNF2 = 0x90
CNF3 = 0x02

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
au.getVoltage()
print(au.getVoltage())

au.setEFLG(0x00)
au.setTXBnCTRL(0x00)
au.getTEC()
au.getREC()
au.getEFLG()


