# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProxyBackendDeviceType(models.Model):
    _name = "proxy.backend_device_type"
    _description = "Proxy Backend Device Type"

    name = fields.Char(
        string="Device Type",
        required=True,
    )
    special = fields.Boolean(
        string="Special Configuration Required",
    )
    description = fields.Text(
        string="Description"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
