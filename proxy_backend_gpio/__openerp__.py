# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Backend Using Hardware Proxy + GPIO",
    "version": "8.0.1.1.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "proxy_backend"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/proxy_backend_device_type_data.xml",
        "views/proxy_backend_raspberry_relay_views.xml",
        "views/proxy_backend_gpio.xml"
    ],
}
