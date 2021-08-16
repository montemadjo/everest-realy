# -*- coding: latin-1 -*-
# pozdrav domaćine! Dal li me se sećaš?
import RPi.GPIO as GPIO
import time
import zmq
import sys

print("miki~!")
print("starting relay app...")

if len(sys.argv) != 4:
    print("cannot proceed - usage: python relay.py ID IPADDRESS PORT")
    sys.exit()

# Argv 1 == id
myId = sys.argv[1]
# Python 2 - ascii bytes to unicode str
if isinstance(myId, bytes):
    myId = myId.decode('ascii')

# Argv 2 == ipaddress
ipaddress = sys.argv[2]
# Python 2 - ascii bytes to unicode str
if isinstance(ipaddress, bytes):
    ipaddress = ipaddress.decode('ascii')

# Argv 3 == port
port = sys.argv[3]
# Python 2 - ascii bytes to unicode str
if isinstance(port, bytes):
    port = port.decode('ascii')

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

# zmq komunikacija
# context = zmq.Context()

# #  Socket to talk to server
# print("Connecting to hello world server…")
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://192.168.1.189:4444")

# #  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")
#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from PACKOM...")
socket.connect("tcp://" + ipaddress + ":" + port)

print("Connected to: " + "tcp://" + ipaddress + ":" + port)

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else ""

# Python 2 - ascii bytes to unicode str
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process updates
while True:
    print("pokušaj primanja poruke...")
    string = socket.recv_string()
    print("primljena poruka")
    sender, command = string.split()
    print("command " + command + " unit# " + sender + " executing...")
    if command == "OPEN":
        print("isljučujem pin 17")
        GPIO.output(17, GPIO.LOW)
        time.sleep(5)

        print("uključujem pin 17")
        GPIO.output(17, GPIO.HIGH)
        time.sleep(5)

GPIO.cleanup()
