# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.exceptions import Warning as UserError


class ProxyBackend(models.Model):
    _inherit = "proxy.backend"

    @api.model
    def get_content_ecspos(self, report_name, object_id, copies=1):
        aeroo = self.get_aeroo_report(report_name, object_id)

        if aeroo["format"] == "raw":
            result = aeroo["content"]
        else:
            raise UserError("Content should be Raw. Please try again.")
        return result
