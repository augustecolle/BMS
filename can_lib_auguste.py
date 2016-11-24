import spidev
import time
import RPi.GPIO as GPIO
import numpy as np
import sys

global spi
global spi2
global currentoffset
global already_initiated
global already_calibrated
already_calibrated = 0
already_initiated = 0
currentoffset = 0


def twos_comp(val, bits):
    '''compute 2's compliment'''
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def startSpi(maxSpeed = 5000000, n = 0):
    '''Starts SPI communication in mode (0,0) at maxSpeed Hz, returns spidev object'''
    if (n==0):
        global spi
        spi = spidev.SpiDev() # create spi object
        spi.open(0, n) # open spi port 0, device (CS) 0 (not used)
        spi.mode = 0b00
        spi.max_speed_hz = maxSpeed
        return spi
    elif (n==1):
        global spi2
        spi2 = spidev.SpiDev() # create spi object
        spi2.open(0, n) # open spi port 0, device (CS) 0 (not used)
        spi2.mode = 0b00
        spi2.max_speed_hz = maxSpeed
        return spi2
    return -1

def softReset():
    '''software reset, returns nothing'''
    global spi
    spi.xfer2([0xC0])

def extendedID(bool = True, n = 0):
    '''CAN with extended Identifier'''
    if bool:
        ans = spi.xfer2([0x02, (3+n)*16 + 2, (int(getTXBnSIDL(), 2) | 0x08)])
    else:
        ans = spi.xfer2([0x02, (3+n)*16 + 2, (int(getTXBnSIDL(), 2) & (~0x08 & 0xFF))])
    return getTXBnSIDL(n)

def getVoltage(n = 0):
    resp = getRXBnDM(n)
    #print(bin((int(resp[0], 2) & 0x1F) << 17))
    #print(bin(((int(resp[0], 2) & 0x1F) << 17) | (int(resp[1], 2) << 9)))
    #print(bin(((int(resp[0], 2) & 0x1F) << 17) | (int(resp[1], 2) << 9) | (int(resp[2], 2) << 1)))
    tot = ((int(resp[0], 2) & 0x1F) << 17) | (int(resp[1], 2) << 9) | (int(resp[2], 2) << 1) | (int(resp[3], 2) >> 7)
    return (twos_comp(tot, 22))*4.096/2.0**21

def getVoltageMaster():
    GPIO.output(25, GPIO.HIGH) #slave select current measurement
    setBFPCTRL(int(getBFPCTRL(), 2) & 0xEF)
    #print(hex(int(getBFPCTRL(), 2)))
    time.sleep(0.10)
    resp = spi2.xfer2([0x00, 0x00, 0x00, 0x00])
    #print(resp)
    tot = ((resp[0] & 0x1F) << 17) | (resp[1] << 9) | (resp[2] << 1) | (resp[3] >> 7)
    #print(bin((int(resp[0], 2) & 0x1F) << 17))
    #print(bin(((int(resp[0], 2) & 0x1F) << 17) | (int(resp[1], 2) << 9)))
    #print(bin(((int(resp[0], 2) & 0x1F) << 17) | (int(resp[1], 2) << 9) | (int(resp[2], 2) << 1)))
    setBFPCTRL(int(getBFPCTRL(), 2) | 0x10)
    return (twos_comp(tot, 22))*4.096/2.0**21


#------------------------WRITE OPERATIONS----------------------


def setCNF1(value):
    ans = spi.xfer2([0x02, 0x2A, value])
    return getCNF1()

def setCNF2(value):
    ans = spi.xfer2([0x02, 0x29, value])
    return getCNF2()

def setCNF3(value):
    ans = spi.xfer2([0x02, 0x28, value])
    return getCNF3()

def setEFLG(value):
    '''set EFLG register'''
    ans = spi.xfer2([0x02, 0x2D, value])
    return getEFLG()

def setCANCTRL(value):
    '''set CANCTRL register'''
    global spi
    ans = spi.xfer2([0x02, 0x0F, value])
    return getCANCTRL()

def setCANINTE(value):
    '''set CANINTE register'''
    ans = spi.xfer2([0x02, 0x2B, value])
    return getCANINTE()

def setTXBnCTRL(value, n = 0):
    '''3 transmit controll registers so n<=2'''
    ans = 0
    if (n <= 2):
        ans = spi.xfer2([0x02, 16*(n+3), value])
    return getTXBnCTRL(n)

def setRXBnCTRL(value, n = 0):
    '''set receive buffer controll register, n<=1'''
    ans = 0
    if (n <= 1):
        ans = spi.xfer2([0x02, (6+n)*16, value])
    return getRXBnCTRL(n)

def setTXRTSCTRL(value):
    '''only lowest 3 bits canare read/write, the rest is read only'''
    if (int(value) <= 7):
        ans = spi.xfer2([0x02, 13, value])
    return getTXRTSCTRL()

def setTXBnSIDH(value, n = 0):
    '''3 transmit SIDH registers so n <= 2'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 1, value])
    return getTXBnSIDH(n)

def setTXBnSIDL(value, n = 0):
    '''3 transmit SIDH registers so n <= 2'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 2, value])
    return getTXBnSIDL(n)

def setTXBnEID8(value, n = 0):
    '''3 transmit EID8 registers so n <= 2'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 3, value])
    return getTXBnEID8(n)

def setTXBnEID0(value, n = 0):
    '''3 transmit EID0 registers so n <= 2'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 4, value])
    return getTXBnEID0(n)

def setTXBnDLC(value, n = 0):
    '''3 transmit DLC registers so n <= 2'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 5, value])
    return getTXBnDLC(n)

def setTXBnDM(value, n = 0):
    '''3 transmit DM registers so n <= 2, value is an array of 8 bytes [byte1, byte2, ..., byte8]'''
    if (n <= 2):
        ans = spi.xfer2([0x02, (3+n)*16 + 6, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]])
    return getTXBnDM(n)

def setCANINTF(value):
    ans = spi.xfer2([0x02, 0x2C, value])
    return getCANINTF()

def setBFPCTRL(value):
    global spi
    ans = spi.xfer2([0x02, 0x0C, value])
    return getBFPCTRL()

def setRXF0SIDH(value):
    ans = spi.xfer2([0x02, 0x00, value])
    return getRXFnSIDH()

def setRXF0SIDL(value):
    ans = spi.xfer2([0x02, 0x01, value])
    return getRXFnSIDL()

def setRXF0EID8(value):
    ans = spi.xfer2([0x02, 0x02, value])
    return getRXFnEID8()

def setRXF0EID0(value):
    ans = spi.xfer2([0x02, 0x03, value])
    return getRXFnEID0()

def setRXM0SIDH(value):
    ans = spi.xfer2([0x02, 0x20, value])
    return getRXFnSIDH()

def setRXM0SIDL(value):
    ans = spi.xfer2([0x02, 0x21, value])
    return getRXFnSIDL()

def setRXM0EID8(value):
    ans = spi.xfer2([0x02, 0x22, value])
    return getRXFnEID8()

def setRXM0EID0(value):
    ans = spi.xfer2([0x02, 0x23, value])
    return getRXFnEID0()


#------------------------READ OPERATIONS-----------------------

def getRXF0SIDH():
    ans = spi.xfer2([0x03, 0x00, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXF0SIDL():
    ans = spi.xfer2([0x03, 0x01, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXF0EID8():
    ans = spi.xfer2([0x03, 0x02, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXF0EID0():
    ans = spi.xfer2([0x03, 0x03, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXM0SIDH():
    ans = spi.xfer2([0x03, 0x20, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXM0SIDL():
    ans = spi.xfer2([0x03, 0x21, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXM0EID8():
    ans = spi.xfer2([0x03, 0x22, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXM0EID0():
    ans = spi.xfer2([0x03, 0x23, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCNF1():
    ans = spi.xfer2([0x03, 0x2A, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCNF2():
    ans = spi.xfer2([0x03, 0x29, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCNF3():
    ans = spi.xfer2([0x03, 0x28, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getEFLG():
    ans = spi.xfer2([0x03, 0x2D, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getBFPCTRL():
    ans = spi.xfer2([0x03, 0x0C, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCANCTRL():
    global spi
    ans = spi.xfer2([0x03, 0x0F, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCANINTF():
    ans = spi.xfer2([0x03, 0x2C, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCANINTE():
    ans = spi.xfer2([0x03, 0x2B, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getOperationMode():
    ''' returns operation mode'''
    global spi
    ans = spi.xfer2([0x03, 0x0E, 0x00])[2]
    return bin(ans >> 5)

def getTXBnDM(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 6, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    return [bin(ans[2+x])[2:].zfill(8) for x in range(8)]

def getTXBnDLC(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 5, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXBnEID0(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 4, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXBnEID8(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 3, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXBnSIDL(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 2, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXBnSIDH(n = 0):
    ans = spi.xfer2([0x03, (3+n)*16 + 1, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXRTSCTRL():
    ans = spi.xfer2([0x03, 13, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getTXBnCTRL(n = 0):
    ans = 0
    if (n <= 2):
        ans = spi.xfer2([0x03, 16*(n+3), 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnCTRL(n = 0):
    '''2 read controll registers so n<=2'''
    ans = 0
    if (n <= 1):
        ans = spi.xfer2([0x03, 16*(n+6), 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnSIDH(n = 0):
    '''two RXBnSIDH registers so n<=1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 1, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnSIDL(n = 0):
    '''two RXBnSIDL registers so n <= 1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 2, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnEID8(n = 0):
    '''two RXBnEID8 registers so n <= 1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 3, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnEID0(n = 0):
    '''two RXBnEID registers so n <= 1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 4, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnDLC(n = 0):
    '''two read DLC registers so n <= 1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 5, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getRXBnDM(n = 0):
    '''two read RXBnDM registers so n <= 1'''
    ans = 0
    if (n<=1):
        ans = spi.xfer2([0x03, (6+n)*16 + 6, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    return [bin(ans[2 + x])[2:].zfill(8) for x in range(8)]

def getTEC():
    ans = 0
    ans = spi.xfer2([0x03, 0x1C, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getREC():
    ans = 0
    ans = spi.xfer2([0x03, 0x1D, 0x00])
    return bin(ans[2])[2:].zfill(8)

def getCurrent():
    global currentoffset
    GPIO.output(25, GPIO.LOW)    
    IPN = 200 #nominal current LEM HAIS
    resp = 0
    time.sleep(0.10)
    resp = spi2.xfer2([0x00, 0x00, 0x00, 0x00])
    #print(resp)
    tot = ((resp[0] & 0x1F) << 17) | (resp[1] << 9) | (resp[2] << 1) | (resp[3] >> 7)
    GPIO.output(25, GPIO.HIGH)
    return ((twos_comp(tot, 22))*1.250/2.0**21*IPN/0.625 - currentoffset)

def getData():
    resp = 0
    resp = spi2.xfer2([0x00, 0x00, 0x00, 0x00])
    return resp

def currentCal(n = 10):
    '''Calculate current offset with no load, returns mean value and standard deviation of n samples'''
    global currentoffset
    global already_calibrated
    pop = []
    for x in range(n):
        pop.append(getCurrent())
    std = np.std(pop)
    meanvalue = np.mean(pop)
    if (not already_calibrated):
        currentoffset = meanvalue
        already_calibrated = already_calibrated + 1
    else:
        currentoffset = currentoffset + meanvalue
    return [meanvalue, std, pop]

def callback_can(channel):
    slave = int(getRXBnEID0(), 2)
    message = int(getRXBnSIDL(), 2)
    print("Interrupt received!")
    print("Message from slave: " + str(slave))
    answer = "Slave says: "
    if (message & 0x80):
        answer = answer + "I've sent you my voltage measurement " + str(getVoltage())
    elif (message & 0x40):
        answer = answer + "I've disabled bleeding"
    elif (message & 0x20):
        anser = answer + "I've enabled bleeding"
    else:
        anser = answer + "Contact auguste.colle@kuleuven.be, something went wrong"
    setCANINTF(0x00)
    print(answer)

    
def getSlaveVoltage(slaveaddresses = [0x01]):
    setTXBnDM([3 for x in range(8)], 0)
    for slave in slaveaddresses:
        setCANINTF(0x00)
        setTXBnEID0(slave)
        setTXBnCTRL(0x0B) 

def master_init(CNF1=0x0F, CNF2=0x90, CNF3=0x02):
    '''initiate master, first function to be called. Sets up the GPIO pins, interrupt routines and BFPCTRL which controlls the state of the bleeding resistor and de slave select of the analog ADC'''
    global already_initiated
    startSpi(10000, 0)
    startSpi(10000, 1)
    if (already_initiated == 0):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(4, GPIO.IN)
        GPIO.setup(25, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(25, GPIO.HIGH) #slave select current measurement
        GPIO.add_event_detect(4, GPIO.FALLING)
        GPIO.add_event_callback(4, callback = callback_can)
        already_initiated = 1
        softReset()
        setCANCTRL(0x80) #set configuration mode
        setCANINTE(0x03) #enable interrupts on receive full
        extendedID()        #enable extended identifier
        setCANINTF(0x00) #clear all interrupt flags
        setRXBnCTRL(0x64)    #accept all incomming messages and enable roll over
        setCNF1(CNF1)    #Used to be:0x0F 
        setCNF2(CNF2)    #Used to be:0x90
        setCNF3(CNF3)    #Used to be:0x02
        setTXBnSIDH(0x00, 0) #set standard identifier 8 high bits
        setTXBnSIDL(0x08, 0) #set low 3 bits stid and extended identifier
        setTXBnEID8(0x00, 0)
        setTXBnDLC(0x01, 0)  #Transmitted message will be a dataframe with 1 byte
        setCANCTRL(0x00)
        setCANINTF(0x00)
        setBFPCTRL(0x0C)
    return 0

def master_exit():
    '''Should be called at the end of a program for a clean exit'''
    global already_initiated
    already_initiated = 0
    GPIO.cleanup()
    sys.exit(0)
