# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from lxml import etree


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type='form', toolbar=False, submenu=False
    ):
        res = super(ResUsers, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='cups_printer_id']"):
            active_ids = self._context.get('active_ids')
            domain = "[('id', '=', 0)]"
            node.set('domain', domain)
        res['arch'] = etree.tostring(doc)
        return res

    @classmethod
    def _build_model(cls, pool, cr):
        model = super(ResUsers, cls)._build_model(pool, cr)
        ModelCls = type(model)
        ModelCls.SELF_WRITEABLE_FIELDS += ["cups_printer_id"]
        return model

    cups_printer_id = fields.Many2one(
        comodel_name="proxy.cups_printer",
        string="Default Cups Printer"
    )

    @api.onchange("proxy_backend_id")
    def onchange_cups_printer_id(self):
        self.cups_printer_id = False
        return {
            "domain": {
                "cups_printer_id": [
                    ("backend_id", "=", self.proxy_backend_id.id)
                ]
            }
        }
