# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Hardware Proxy for Backend",
    "version": "8.0.1.4.1",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/proxy_backend.xml",
        "views/proxy_backend_views.xml",
        "views/proxy_backend_device_views.xml",
        "views/proxy_backend_device_type_views.xml",
        "views/res_users_views.xml"
    ],
    "qweb": [
        "static/src/xml/proxy_backend_widget.xml",
    ],
}
