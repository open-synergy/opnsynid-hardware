# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProxyBackend(models.Model):
    _name = "proxy.backend"
    _description = "Proxy Backend"

    name = fields.Char(
        string="Name",
        required=True,
    )
    backend_ip = fields.Char(
        string="IP Address",
        required=True,
        help='IP Address Of The Hardware Proxy'
    )
    description = fields.Text(
        string="Description"
    )
    user_ids = fields.One2many(
        string="Users",
        comodel_name="res.users",
        inverse_name="proxy_backend_id",
        )
    active = fields.Boolean(
        string="Active",
        default=True
    )
