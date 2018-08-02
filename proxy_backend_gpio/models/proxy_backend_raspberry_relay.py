# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ProxyBackendRaspberryRelay(models.Model):
    _name = "proxy.backend_raspberry_relay"
    _inherits = {"proxy.backend_device": "device_id"}
    _description = "Proxy Backend Device - Raspberry Relay"

    @api.model
    def _default_device_type(self):
        return self.env.ref("proxy_backend_gpio."
                            "proxy_backend_device_type_"
                            "raspberry_relay").id

    device_id = fields.Many2one(
        string="Device",
        comodel_name="proxy.backend_device",
        required=True,
        ondelete="cascade",
    )
    dummy_device_id = fields.Many2one(
        string="ID Device",
        comodel_name="proxy.backend_device",
        related="device_id",
        )
    pin = fields.Integer(
        string="Pin",
    )

