# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ProxyBackendDevice(models.Model):
    _name = "proxy.backend_device"
    _description = "Proxy Backend Device"

    @api.model
    def _default_device_type(self):
        context = self._context
        if context.get("device_type"):
            return context["device_type"]
        else:
            return False

    name = fields.Char(
        string="Device Name",
        required=True,
    )
    type_id = fields.Many2one(
        string="Device Type",
        comodel_name="proxy.backend_device_type",
        required=True,
        default=lambda self: self._default_device_type(),
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
