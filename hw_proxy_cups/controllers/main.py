# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging
import time
from threading import Thread, Lock
from Queue import Queue
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from openerp import http
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

try:
    import cups
except (ImportError, IOError) as err:
    logger.debug(err)


class CupsDriver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock = Lock()

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def push_task(self, task, data=None, printer_name=None):
        self.lockedstart()
        self.queue.put((time.time(), task, data, printer_name))

    def print_using_cups(self, data, printer_name):
        try:
            conn = cups.Connection()
            with NamedTemporaryFile() as f:
                f.write(data.decode('base64'))
                f.flush()
                conn.printFile(printer_name, f.name, "Aeroo Print Cups", {})
        except Exception as e:
            logger.error('Error: %s' % str(e))

    def run(self):
        while True:
            try:
                timestamp, task, data, printer_name =\
                    self.queue.get(True)
                if task == 'print_using_cups':
                    self.print_using_cups(data, printer_name)
                else:
                    pass
            except Exception as e:
                logger.error('Error: %s' % str(e))


driver = CupsDriver()


class CupsProxy(hw_proxy.Proxy):
    @http.route(
        '/hw_proxy/print_using_cups', type='json', auth='none',
        cors='*')
    def print_using_cups(self, data, printer_name):
        driver.push_task('print_using_cups', data, printer_name)

    @http.route(
        '/hw_proxy/get_printer_cups', type='json', auth='none',
        cors='*')
    def get_printer_cups(self):
        printers = {}
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            printer_name = printers.keys()
            logger.info(
                'Request get printer %s',
                printer_name)
        except Exception as e:
            logger.error('Error: %s' % str(e))
        return printers
