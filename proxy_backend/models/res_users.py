# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def _build_model(cls, pool, cr):
        model = super(ResUsers, cls)._build_model(pool, cr)
        ModelCls = type(model)
        ModelCls.SELF_WRITEABLE_FIELDS += ["proxy_backend_id"]
        return model

    proxy_backend_id = fields.Many2one(
        comodel_name="proxy.backend",
        string="Default Proxy"
    )
