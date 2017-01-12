import serial as serial
import time
import copy
import binascii


DevNode = "00" #device node, manual configured on machine, standard value is 01
pause = 0.02 #used for a timeout between sending command and reading buffer for the response
vNom = 720 #on machine, nominal votage
iNom = 15
pNom = 3000


def startSerial(port = '/dev/ttyUSB0', devicenode = "01"):
    '''Initialize serial communication with the default values on page 28 of the programming manual. The devicenode (global DevNode, a two character string) is standard set to "01" but is device dependent, the port is standard set to /dev/ttyUSB0 cause this program was written on a linux distribution'''
    global DevNode
    global ser
    DevNode = devicenode 
    ser = serial.Serial(port, baudrate=57600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=0)
    return ser


def stopSerial():
    '''Stops serial communication'''
    global ser
    ser.close()
    return 0


def clearBuffer():
    ser.flushInput()
    ser.flushOutput()

def readAndTreat(maxbytes = 20):
    '''Reads and treats the incomming data. The default value for the maximum on incomming bytes is arbitrary set to 100, although not so arbitrary since I think a larger response from the device is not possible unless one forgets to read the buffer. Returns the treated data as an array of hex numbers'''
    time.sleep(0.05)
    inBuffer = ser.read(maxbytes)
    inBuffer = binascii.hexlify(inBuffer).decode('UTF-8')
    inBuffer = [inBuffer[i:i+2] for i in range(0, len(inBuffer), 2)]
    return inBuffer


def getActualValues():
    '''get voltage, current and power. These are read only'''
    global DevNode
    global vNom
    global iNom
    global pNom
    global pause

    SD = b'\x55'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x47'
    #no data object in querying, see manual page 28
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    time.sleep(0.05)
    ser.write(get_query)
    treatedData = readAndTreat()
    voltage = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*vNom/25600.0
    current = int((treatedData[5]+treatedData[6]).replace("0x",""), 16)*iNom/25600.0
    power = int((treatedData[7]+treatedData[8]).replace("0x",""), 16)*pNom/25600.0
    return [voltage, current, power]


def setVoltage(voltage):
    '''set voltage, expects float value in Volts'''
    global DevNode
    global vNom
    global pause

    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x32'
    setValue = hex(int(voltage*25600.0/vNom)).replace("0x","").zfill(4)
    DATA1 = str(bytearray.fromhex(setValue[:2]))
    DATA2 = str(bytearray.fromhex(setValue[2:]))
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setCurrent(current):
    '''set current, expects float value in Amps'''
    global DevNode
    global iNom
    global pause
    if (current < 0):
        return 1 #current cant be smaller than zero
    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x33'
    setValue = hex(int(current*25600.0/iNom)).replace("0x","").zfill(4)
    DATA1 = str(bytearray.fromhex(setValue[:2]))
    DATA2 = str(bytearray.fromhex(setValue[2:]))
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setPower(power):
    '''set power, expects float value in Watts'''
    global DevNode
    global pNom
    global pause

    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x34'
    setValue = hex(int(power*25600.0/pNom)).replace("0x","").zfill(4)
    DATA1 = str(bytearray.fromhex(setValue[:2]))
    DATA2 = str(bytearray.fromhex(setValue[2:]))
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setMaxVoltage(maxvoltage):
    '''set maximum voltage, expects float value in Volts'''
    global DevNode
    global vNom
    global pause

    powerOff() #necessary to edit the voltage limit
    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x1D'
    setValue = hex(int(maxvoltage*25600.0/vNom)).replace("0x","").zfill(4)
    DATA1 = str(bytearray.fromhex(setValue[:2]))
    DATA2 = str(bytearray.fromhex(setValue[2:]))
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    powerOn() #turn power back on
    return 0;


def setMaxCurrent(maxcurrent):
    '''set maximum current, expects float value in Amps'''
    global DevNode
    global iNom
    global pause

    powerOff() #necessary to edit the voltage limit
    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x1D'
    setValue = hex(int(maxcurrent*25600.0/iNom)).replace("0x","").zfill(4)
    DATA1 = str(bytearray.fromhex(setValue[:2]))
    DATA2 = str(bytearray.fromhex(setValue[2:]))
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    powerOn() #turn power back on
    return 0;


def powerOff():
    '''Puts the device in power output OFF mode'''
    global DevNode
    global pause

    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x36'
    DATA1 = b'\x01'
    DATA2 = b'\x00'
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0   


def powerOn():
    '''Puts the device in power output ON mode'''
    global DevNode
    global pause

    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x36'
    DATA1 = b'\x01'
    DATA2 = b'\x01'
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0   


def getVoltage():
    '''get actual voltage in volts on DC bus'''
    return getActualValues()[0]


def getCurrent():
    '''get actual current in amps'''
    return getActualValues()[1]


def getPower():
    '''get actual power in Watt'''
    return getActualValues()[1]


def getSetVoltage():
    '''Get set value of voltage'''
    global DevNode
    global vNom
    global pause
    SD = b'\x51'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x32'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    time.sleep(pause)
    treatedData = readAndTreat()
    voltage = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*vNom/25600
    time.sleep(pause)
    clearBuffer()
    return voltage;


def remoteControllOn():
    '''Enable remote controll'''
    global DevNode
    global pause

    SD = b'\xD1'
    DN = str(bytearray.fromhex(DevNode))
    OBJ = b'\x36'
    DATA1 = b'\x10'
    DATA2 = b'\x10'
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    time.sleep(pause)
    return 0   


def checksum(dataList):
    '''calculates checksum and returns it'''
    checksum = 0 
    for hexVal in dataList:
        checksum += int(binascii.hexlify(hexVal).decode('UTF-8'), 16)
    checksum = hex(checksum)[2:].zfill(4)
    return str(bytearray.fromhex(checksum))


def main():
    startSerial()
    return 0


#if this script is not imported as a module run main
if __name__ == "__main__":
    main()
