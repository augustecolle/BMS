import os
import subprocess
import signal

def get_pid(name):
    return map(int, subprocess.check_output(["pidof", name]).split())

for x in get_pid("python"):
    print(os.getpid())
    print(x)
    print(int(x))
    print(type(x))
    print(type(os.getpid()))
    if (int(x) != int(os.getpid())):
        os.kill(int(x), signal.SIGTERM)


