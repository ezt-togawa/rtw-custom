from odoo import models, api
from odoo.exceptions import UserError


class PurchaseExportExcel(models.TransientModel):
    _name = 'purchase.export.excel.wizard' 
    _description = 'Wizard for Exporting Purchase Excel'

    @api.model
    def export_excel(self, docids, model):
        records = self.env[model].browse(docids)
        if len(records) > 1:
            partners = records.mapped('order_id.partner_id.id' if model == 'purchase.order.line' else 'partner_id.id')

            destinations = (records.mapped('destination_purchase_order_line') if model == 'purchase.order.line' else records.mapped('order_line.destination_purchase_order_line'))

            if len(set(partners)) > 1:
                raise UserError('仕入先が複数にまたがるため出力できません。')
            if len(set(destinations)) > 1:
                raise UserError('送り先（納入先）が複数にまたがるため出力できません。')
        if(model == 'purchase.order.line'):
            report_ref = self.env.ref('rtw_excel_report.purchase_order_line_component_2')
        else:
            report_ref = self.env.ref('rtw_excel_report.purchase_order_component')
        action = report_ref.report_action(records.ids if records else docids, None, False)

        return action
