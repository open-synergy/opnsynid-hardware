# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    proxy_backend_id = fields.Many2one(
        comodel_name="proxy.backend",
        string="Default Proxy"
    )
