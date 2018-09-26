# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, _
from openerp.exceptions import Warning as UserError
import base64


class ProxyBackend(models.Model):
    _inherit = "proxy.backend"

    cups_printer_ids = fields.One2many(
        string="Cups Printers",
        comodel_name="proxy.cups_printer",
        inverse_name="backend_id",
    )

    @api.model
    def get_content_cups(self, report_name, object_id, params=None, copies=1):
        aeroo = self.get_aeroo_report(report_name, object_id, params)

        if aeroo["format"] != "raw":
            result = base64.encodestring(aeroo["content"])
        else:
            raise UserError(_("Content shouldn't be Raw. Please try again."))
        return result
