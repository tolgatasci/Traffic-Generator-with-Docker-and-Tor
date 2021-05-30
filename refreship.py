#!/usr/bin/python3
from stem import Signal
from stem.control import Controller
import time
with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="abcdef")
        controller.signal(Signal.NEWNYM)
time.sleep(25)