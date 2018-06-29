# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProxyBackendSerialRelayChannel(models.Model):
    _name = "proxy.backend_serial_relay_channel"
    _description = "Proxy Backend Serial Relay Channel"

    name = fields.Integer(
        string="Pin",
    )
    device_id = fields.Many2one(
        string="Serial Relay",
        comodel_name="proxy.backend_serial_relay",
    )
