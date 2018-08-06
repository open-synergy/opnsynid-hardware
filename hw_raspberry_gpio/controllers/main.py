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
    import RPi.GPIO as GPIO
except (ImportError, IOError, RuntimeError) as err:
    logger.debug(err)


class RpiGpioDriver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock = Lock()

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def push_task(self, task, channel, mode, interval=0):
        self.lockedstart()
        self.queue.put((time.time(), task, channel, mode, interval))

    def rpi_gpio_out_on(self, channel, mode):
        try:
            if mode == "board":
                GPIO.setmode(GPIO.BOARD)
            else:
                GPIO.setmode(GPIO.BCM)
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, GPIO.LOW)
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def rpi_gpio_out_off(self, channel, mode):
        try:
            if mode == "board":
                GPIO.setmode(GPIO.BOARD)
            else:
                GPIO.setmode(GPIO.BCM)
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, GPIO.HIGH)
            GPIO.cleanup(channel)
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def rpi_gpio_out_on_off_timer(self, channel, mode, interval):
        try:
            GPIO.setmode(mode)
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, GPIO.HIGH)
            time.sleep(interval)
            GPIO.output(channel, GPIO.LOW)
            GPIO.cleanup(channel)
        except Exception as e:
            logger.error("Error: %s" % str(e))

    def run(self):
        while True:
            try:
                timestamp, task, channel, mode, interval = self.queue.get(True)
                if task == "rpi_gpio_out_on":
                    self.rpi_gpio_out_on(channel, mode)
                elif task == "rpi_gpio_out_off":
                    self.rpi_gpio_out_off(channel, mode)
                if task == "rpi_gpio_out_on_off_timer":
                    self.rpi_gpio_out_on_off_timer(channel, mode, interval)
                else:
                    pass
            except Exception as e:
                logger.error("Error: %s" % str(e))


driver = RpiGpioDriver()


class RpiGpioProxy(hw_proxy.Proxy):

    @http.route(
        "/hw_proxy/rpi_gpio_out_on", type="json", auth="none",
        cors="*")
    def rpi_gpio_out_on(self, channel, mode="board"):
        driver.push_task("rpi_gpio_out_on", channel, mode)

    @http.route(
        "/hw_proxy/rpi_gpio_out_off", type="json", auth="none",
        cors="*")
    def rpi_gpio_out_off(self, channel, mode="board"):
        driver.push_task("rpi_gpio_out_off", channel, mode)

    @http.route(
        "/hw_proxy/rpi_gpio_out_on_off_timer", type="json", auth="none",
        cors="*")
    def rpi_gpio_out_on_off_timer(self, channel, mode=None, interval=None):
        driver.push_task("rpi_gpio_out_on_off_timer", channel, mode, interval)
