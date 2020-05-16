import subprocess
import os
import sys
import time
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzstatus import FritzStatus
from getpass import getpass

if os.geteuid() != 0:
    print("We need to be root for changing ip routes. Exiting..")
    sys.exit()

FNULL = open(os.devnull, 'w')

PING_TEST_HOST = os.environ.get('FO_PING_HOST', '8.8.8.8')
FRITZBOX_GATEWAY = os.environ.get('FRITZBOX_GATEWAY', '192.168.178.1')
FAILOVER_GATEWAY = os.environ.get('FAILOVER_GATEWAY', '192.168.178.10')
INTERFACE = os.environ.get('FO_INTERFACE', 'enp3s0')
FRITZBOX_PASSWORD = os.environ.get(
    'FRITZBOX_PASSWORD', getpass(prompt='FritzBox Password: '))

DELAY = 60

conn = FritzConnection(address=FRITZBOX_GATEWAY, password=FRITZBOX_PASSWORD)
status = FritzStatus(conn)


def changeGateway(gateway):
    subprocess.call(['ip', 'route', 'change',
                     'default', 'via', gateway, 'dev', INTERFACE])
    subprocess.call(['ip', 'route', 'flush', 'cache'])
    print("changed gateway to: {}".format(gateway))


def testPing():
    return subprocess.run(['ping', '-4', '-c', '1', '-w', '3', '-q', PING_TEST_HOST], stdout=FNULL).returncode == 0


def getCurrentGateway():
    cmd = "ip r l 0/0 | head -1 | cut -f3 -d\' \'"
    ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return ps.communicate()[0].rstrip().decode()


def check():
    currentGateway = getCurrentGateway()
    if status.is_connected:
        if currentGateway == FAILOVER_GATEWAY:
            changeGateway(FRITZBOX_GATEWAY)
            if testPing() == False:  # If FRITZBOX_GATEWAY fails ping, switch back.
                print("Ping verification failed. Going back to failover...")
                changeGateway(FAILOVER_GATEWAY)
        elif currentGateway == FRITZBOX_GATEWAY:
            if testPing() == False:
                print("Ping verification failed. Switching to failover...")
                changeGateway(FAILOVER_GATEWAY)
            else:
                print("Connection via {} is healthy".format(currentGateway))
        else:
            print("Current gateway not known!")
    else:
        print("FritzBox is NOT connected")
        if currentGateway == FRITZBOX_GATEWAY:
            changeGateway(FAILOVER_GATEWAY)
        else:
            print("Current gateway not known!")


def loopCheck():
    while True:
        print("\nChecking...")
        check()
        print("waiting {} seconds...".format(DELAY))
        time.sleep(DELAY)


if __name__ == '__main__':
    try:
        loopCheck()
    except KeyboardInterrupt:
        print('Interrupted.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
