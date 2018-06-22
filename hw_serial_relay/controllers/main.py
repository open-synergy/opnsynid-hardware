# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging
import time
from threading import Thread, Lock
from Queue import Queue
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from openerp import http

logger = logging.getLogger(__name__)

try:
    import serial
except (ImportError, IOError, RuntimeError) as err:
    logger.debug(err)


class SerialRelayDriver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock = Lock()
        self.start_marker = 60
        self.end_marker = 62

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def push_task(self, task, port, pin, delay):
        self.lockedstart()
        self.queue.put((time.time(), task, port, pin, delay))

    def setup_relay(self, serial_device, pin):
        message = "<%s,%s,%s,%s>" % (0, pin, 0, 0)
        self.send_to_serial_device(serial_device, message)
        while serial_device.inWaiting() == 0:
            pass
        data = self.receive_from_serial_device(serial_device)
        return data

    def serial_relay_on(self, port, pin, delay):
        try:
            serial_device = self.open_serial_device(port)
            msg1 = self.wait_for_arduino(serial_device)
            logger.info(msg1)
            msg2 = self.setup_relay(serial_device, pin)
            logger.info(msg2)
            message = "<%s,%s,%s,%s>" % (1, pin, 0, delay)
            self.send_to_serial_device(serial_device, message)
            while serial_device.inWaiting() == 0:
                pass
            data = self.receive_from_serial_device(serial_device)
            logger.info(data)

            self.close_serial_device(serial_device)
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def serial_relay_off(self, port, pin, delay):
        try:
            serial_device = self.open_serial_device(port)
            msg1 = self.wait_for_arduino(serial_device)
            logger.info(msg1)
            msg2 = self.setup_relay(serial_device, pin)
            logger.info(msg2)
            message = "<%s,%s,%s,%s>" % (1, pin, 1, delay)
            self.send_to_serial_device(serial_device, message)
            while serial_device.inWaiting() == 0:
                pass
            data = self.receive_from_serial_device(serial_device)
            logger.info(data)

            self.close_serial_device(serial_device)
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def serial_relay_setup(self, port, pin, delay):
        try:
            pass
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def open_serial_device(self, port):
        serial_device = serial.Serial(
            port, "9600")
        if serial_device.isOpen():
            serial_device.close()

        try:
            serial_device.open()
        except Exception as e:
            logger.error("Error: %s" % str(e))
        return serial_device

    def close_serial_device(self, serial_device):
        serial_device.close()

    def wait_for_arduino(self, serial_device):
        msg = ""
        while msg.find("ready") == -1:
            while serial_device.inWaiting() == 0:
                pass

            msg = self.receive_from_serial_device(serial_device)
        return msg

    def receive_from_serial_device(self, serial_device):
        ck = ""
        x = "z"

        while ord(x) != self.start_marker:
            x = serial_device.read()

        while ord(x) != self.end_marker:
            if ord(x) != self.start_marker:
                ck = ck + x.decode("utf-8")
            x = serial_device.read()
        return ck

    def send_to_serial_device(self, serial_device, message):
        serial_device.write(message.encode("utf-8"))

    def run(self):
        while True:
            try:
                timestamp, task, port, pin, delay = self.queue.get(True)
                if task == "serial_relay_on":
                    self.serial_relay_on(port, pin, delay)
                elif task == "serial_relay_off":
                    self.serial_relay_off(port, pin, delay)
            except Exception as e:
                logger.error("Error: %s" % str(e))


driver = SerialRelayDriver()


class SerialRelayProxy(hw_proxy.Proxy):

    @http.route(
        "/hw_proxy/serial_relay_on", type="json", auth="none",
        cors="*")
    def serial_relay_on(self, port, pin, delay):
        driver.push_task("serial_relay_on", port, pin, delay)

    @http.route(
        "/hw_proxy/serial_relay_off", type="json", auth="none",
        cors="*")
    def serial_relay_off(self, port, pin, delay):
        driver.push_task("serial_relay_off", port, pin, delay)
