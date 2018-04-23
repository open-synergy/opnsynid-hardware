# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import os
import base64
from tempfile import mkstemp
from openerp import models, api, _
from openerp.exceptions import except_orm

logger = logging.getLogger(__name__)


class ProxyBackend(models.Model):
    _inherit = "proxy.backend"

    @api.model
    def get_content_aeroo_report(self, report_name, object_id, copies=1):
        logger.info(
            'Values Report %s ID %s',
            report_name, object_id)
        data_id = object_id[0]
        report = self.env['ir.actions.report.xml']._lookup_report(report_name)
        report_xml = self.env['report']._get_report_from_name(report_name)
        data = {
            'model': report_xml.model,
            'id': data_id,
            'report_type': 'aeroo',
        }
        logger.info(
            'Request printing aeroo report %s model %s ID %d in %d copies',
            report_name, data['model'], data['id'], copies)
        aeroo_report_content, aeroo_report_format= report.create(
            self.env.cr, self.env.uid, [data_id],
            data, context=dict(self.env.context))

        #fd, file_name = mkstemp()
        #try:
        #    os.write(fd, aeroo_report_content)
        #finally:
        #    os.close(fd)

        x = base64.encodestring(aeroo_report_content)

        #raise except_orm(_('BUGS'),
        #    _("'%s'") % (x,))
        return x
