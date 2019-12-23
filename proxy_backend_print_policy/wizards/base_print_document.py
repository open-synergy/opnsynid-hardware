# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class BasePrintDocument(models.TransientModel):
    _inherit = "base.print.document"

    @api.model
    def _compute_allowed_printer_ids(self):
        result = []
        user = self.env.user
        obj_proxy_cups_printer =\
            self.env["proxy.cups_printer"]
        backend_id =\
            user.proxy_backend_id.id

        criteria = [
            ("backend_id", "=", backend_id)
        ]
        printer_ids =\
            obj_proxy_cups_printer.search(criteria)

        if printer_ids:
            for printer in printer_ids:
                result.append(printer.id)
        return result

    allowed_printer_ids = fields.Many2many(
        string="Allowed Printers",
        comodel_name="proxy.cups_printer",
        default=lambda self: self._compute_allowed_printer_ids(),
        relation="rel_print_document_2_cups_printer",
        column1="wizard_id",
        column2="printer_id",
    )

    printer_id = fields.Many2one(
        string="Printer(s)",
        comodel_name="proxy.cups_printer",
    )

    @api.multi
    def get_report_name(self):
        return self.report_action_id.report_name

    @api.multi
    def get_printer_name(self):
        return self.printer_id.name

    @api.multi
    def _prepare_context(self):
        self.ensure_one()

        report_name =\
            self.get_report_name()
        printer_name =\
            self.get_printer_name()
        active_id =\
            self.env.context.get("active_id", "")

        return {
            "report_name": report_name,
            "printer_name": printer_name,
            "object_id": [active_id]
        }

    @api.multi
    def action_print_using_proxy(self):
        client_action_ref =\
            self.env.ref(
                "proxy_backend_cups_aeroo."
                "proxy_backend_cups_aeroo_action"
            )
        ctx =\
            self._prepare_context()

        action = client_action_ref.read()[0]
        action.update({'context': ctx})
        return action
