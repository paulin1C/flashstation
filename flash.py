import os, time, argparse

import multiprocessing as mp

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="binary file to flash")
args = parser.parse_args()

portprefix = "/dev/ttyUSB" # for linux, might be diffrent in your OS
portrange = range(10) # /dev/ttyUSB0 to /dev/ttyUSB9

flashcommand = "esptool -b 1500000  --port {} write_flash --flash_mode qio 0x00000 {}"

class Port:
    def __init__(self, path):
        self.path = path
        self.connected = False
    def update(self):
        port_exists = os.path.lexists(self.path)
        if self.connected == port_exists:
            return False # return False when it didn't change
        self.connected = port_exists
        return self.connected # return True when it changed and is connected
    def flash(self):
        print("flashing %s" % self.path)
        # time.sleep(5)
        os.system(flashcommand.format(self.path, args.f))

pool = mp.Pool()

ports = []
for port_id in portrange:
    ports.append(Port(portprefix + str(port_id)))

while True:
    for port in ports:
        if port.update():
            print("port %s connected" % port.path)
            p = pool.apply_async(port.flash)
        time.sleep(0.1)
