# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReportMrpWithoutPayment(models.AbstractModel):
    _name = 'report.custom_report_rtw.report_purchase_order_pdf_list_ab'
    _description = 'report_purchase_order_pdf_list_ab'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'docs': docs,
        }

class ReportMrpWithPayment(models.AbstractModel):
    _name = 'report.custom_report_rtw.report_purchase_order_pdf_list'
    _description = 'report_purchase_order_pdf_list'
    _inherit = 'report.custom_report_rtw.report_purchase_order_pdf_list_ab'

    @api.model
    def _get_report_values(self, docids, data=None):
        rslt = super()._get_report_values(docids, data)
        rslt['report_type'] = data.get('report_type') if data else ''
        return rslt
