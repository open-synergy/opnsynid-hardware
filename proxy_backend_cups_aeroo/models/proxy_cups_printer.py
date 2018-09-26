# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class ProxyCupsPrinter(models.Model):
    _name = "proxy.cups_printer"
    _description = "Proxy Cups Printer"

    name = fields.Char(
        string="Printer Name",
        required=True,
    )
    backend_id = fields.Many2one(
        string="Backend",
        comodel_name="proxy.backend",
        ondelete='cascade'
    )
    state = fields.Selection(
        selection=[
            ('3', 'Idle'),
            ('4', 'Busy'),
            ('5', 'Stopped')],
        string='State'
    )

    @api.model
    def create_from_ui(self, printer, backend_id):
        windows_action =\
            self.env.ref("proxy_backend_cups_aeroo.proxy_backend_view_form")
        if printer:
            result = printer['result']

            criteria = [
                ("backend_id", "=", backend_id["id"])
            ]
            cups_printer =\
                self.search(criteria)
            if cups_printer:
                cups_printer.unlink()

            for data in printer['result']:
                result_data = printer['result'][data]
                val = {
                    "name": data,
                    "backend_id": backend_id["id"],
                    "state": str(result_data["printer-state"])
                }
                self.create(val)
        return windows_action.read()[0]