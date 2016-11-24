import imp
import can_lib_auguste as au
import time

imp.reload(au)

au.master_init()

a = time.time()
for x in range(5):
    au.getSlaveVoltage([0x01, 0x02, 0x03])
    print(au.getVoltageMaster())
    print(au.getCurrent())
    time.sleep(0.10)
b = time.time()
print(b-a)

au.master_exit()

