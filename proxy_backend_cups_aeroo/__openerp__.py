# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Backend Direct Printing Using Hardware Proxy + "
            "Aeroo Report + Cups",
    "version": "8.0.1.2.1",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "proxy_backend_aeroo"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/proxy_backend_cups_aeroo.xml",
        "views/proxy_backend_views.xml",
        "views/res_users_views.xml"
    ],
}
