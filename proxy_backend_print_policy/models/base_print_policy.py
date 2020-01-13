# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class BasePrintPolicy(models.Model):
    _inherit = "base.print.policy"

    proxy_group_ids = fields.Many2many(
        string="Allowed to Print Using Proxy",
        comodel_name="res.groups",
        rel="rel_print_policy_group_proxy",
        col1="print_policy_id",
        col2="group_id",
    )
    escpos_group_ids = fields.Many2many(
        string="Allowed to Print Using Escpos",
        comodel_name="res.groups",
        rel="rel_print_policy_group_escpos",
        col1="print_policy_id",
        col2="group_id",
    )
