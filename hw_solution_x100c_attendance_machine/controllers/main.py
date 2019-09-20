# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging
import time
from threading import Thread, Lock
from Queue import Queue
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from openerp.http import request
from openerp import http
from tempfile import NamedTemporaryFile
import openerp.addons.web.controllers.main as oe_web
from openerp.tools.config import config

logger = logging.getLogger(__name__)

try:
    import requests
    import xml.etree.ElementTree as ET
    import csv
except (ImportError, IOError) as err:
    logger.debug(err)


class X100cDriver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock = Lock()
        self.ethernet_url = config.get(
            "ethernet_url", "")
        self.key = config.get(
            "key", "")

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def push_task(self, task):
        self.lockedstart()
        self.queue.put((time.time(), task))

    def load_attendance_data(self):
        try:
            s = requests.Session()
            url = self.ethernet_url + "/iWsService"
            headers = {"content-type": "text/xml"}
            body = "<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">" + \
                   "%s</ArgComKey>" % (self.key) + \
                   "<Arg><PIN xsi:type=\"xsd:integer\">All</PIN></Arg>" + \
                   "</GetAttLog>"
            response = s.post(url, data=body, headers=headers, timeout=None)
            logger.info(response.content)
            root = ET.fromstring(response.content)

            with NamedTemporaryFile(mode="w+b") as f:
                attendance_writer = csv.writer(
                    f, delimiter=",", quoting=csv.QUOTE_ALL)
                for elem in root.iter("Row"):
                    str_pin = elem.find("PIN").text.encode("utf-8")
                    str_datetime = elem.find("DateTime").text.encode("utf-8")
                    str_status = elem.find("Status").text.encode("utf-8")
                    attendance_writer.writerow(
                        [str_pin, str_datetime, str_status])
                f.seek(0)
                data = f.read()
                f.close()
            content = [
                ("Content-Type", "text/csv;charset=utf-8"),
                ("Content-Disposition", oe_web.content_disposition("a.csv"))
            ]
            return request.make_response(
                data, content)

        except Exception as e:
            logger.error('Error: %s' % str(e))

    def run(self):
        while True:
            try:
                timestamp, task, ethernet_url, key =\
                    self.queue.get(True)
                if task == "load_attendance_data":
                    self.load_attendance_data(ethernet_url, key)
                else:
                    pass
            except Exception as e:
                logger.error('Error: %s' % str(e))


driver = X100cDriver()


class X100cDriver(hw_proxy.Proxy):
    @http.route(
        "/hw_proxy/load_attendance_data", type="http", auth="none",
        cors="*")
    def load_attendance_data(self):
        return driver.load_attendance_data()
