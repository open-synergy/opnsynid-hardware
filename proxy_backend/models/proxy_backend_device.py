# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProxyBackendDevice(models.Model):
    _name = "proxy.backend_device"
    _description = "Proxy Backend Device"

    name = fields.Char(
        string="Serial Number",
        required=True,
    )
    type_id = fields.Many2one(
        string="Device Type",
        comodel_name="proxy.backend_device_type",
        required=True,
    )
    proxy_backend_id = fields.Many2one(
        string="Proxy Backend",
        comodel_name="proxy.backend",
    )
    description = fields.Text(
        string="Description"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
