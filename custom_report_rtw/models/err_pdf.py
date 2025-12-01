from odoo import models 
from odoo.exceptions import UserError 

class error_export_many_pdf(models.Model):
    _inherit = 'ir.actions.report'
    
    def _get_rendering_context(self, docids, data):
        res = super(error_export_many_pdf, self)._get_rendering_context(docids, data)
        if self.model == 'mrp.production':
            list_mrp_origin = []
            for doc in docids:
                mrp = self.env['mrp.production'].search([('id','=',doc)])
                if mrp:
                    list_mrp_origin.append(mrp.mrp_production_so_id.id or '')
            if list_mrp_origin and len(list_mrp_origin) > 1:
                first_element = list_mrp_origin[0]
                if not all(element == first_element for element in list_mrp_origin):
                    raise UserError('販売オーダーが複数にまたがるため出力できません。')
                
        if self.model == 'purchase.order':
            if len(docids) == 1:
                pass
            else:
                list_partner_id = []
                list_destination = []

                for id_purchase in docids:
                    po = self.env['purchase.order'].browse(id_purchase)
                    if po:
                        list_partner_id.append(po.partner_id.id or '')
                        destinations = po.order_line.mapped('destination_purchase_order_line') or []
                        list_destination.extend(destinations)

                if len(set(list_partner_id)) > 1:
                    raise UserError('仕入先が複数にまたがるため出力できません。')

                if len(set(list_destination)) > 1:
                    raise UserError('送り先（納入先）が複数にまたがるため出力できません。')

        elif self.model == 'purchase.order.line':
            if len(docids) == 1:
                pass
            else:
                partner_ids = []
                destination_lines = []

                for line_id in docids:
                    pol = self.env['purchase.order.line'].browse(line_id)
                    partner_ids.append(pol.order_id.partner_id.id)
                    destination_lines.append(pol.destination_purchase_order_line or '')

                if len(set(partner_ids)) > 1:
                    raise UserError('仕入先が複数にまたがるため出力できません。')

                if len(set(destination_lines)) > 1:
                    raise UserError('送り先（納入先）が複数にまたがるため出力できません。')

                
        return res
