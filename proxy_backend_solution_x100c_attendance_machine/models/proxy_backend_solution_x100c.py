# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProxyBackendSolutionX100c(models.Model):
    _name = "proxy.backend_solution_x100c"
    _inherits = {"proxy.backend_device": "device_id"}
    _description = "Proxy Backend Device - Solution X100-C"

    device_id = fields.Many2one(
        string="Device",
        comodel_name="proxy.backend_device",
        required=True,
        ondelete="cascade",
        auto_join=True
    )
    connection_type = fields.Selection(
        string="Connection Type",
        selection=[
            ("ethernet", "Ethernet"),
        ],
        default="ethernet",
        required=True,
    )
    ethernet_url = fields.Char(
        string="URL",
    )
    key = fields.Integer(
        string="Key"
    )
