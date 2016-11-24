import imp
import can_lib_auguste as au
import time

imp.reload(au)

au.master_init()

slaves = [0x01, 0x02, 0x03]
au.init_meting(slaves)
au.exit_meting()

#for some reason I have to put getvoltagemaster and current before getvoltageslaves, otherwise I get false values. Have to check this.

au.currentCal(10)
for x in range(50):
    au.getVoltageMaster()
    au.getCurrent()
    au.getVoltageSlaves([0x01, 0x02, 0x03])
    au.datadict['timestamp'].append(time.time())
    time.sleep(0.10)

print("DONE")
au.master_exit()
