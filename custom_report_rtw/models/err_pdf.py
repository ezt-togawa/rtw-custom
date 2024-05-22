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
            allow_print = False
            if len(docids) == 1:
                allow_print = True
            else: 
                list_partner_id =[]
                for id_purchase in docids:
                    po = self.env['purchase.order'].search([('id','=',id_purchase)])
                    if po:
                        list_partner_id.append(po.partner_id.id or '')

                if list_partner_id:
                    for id in list_partner_id[1:]:
                        if id == list_partner_id[0]:
                            allow_print = True
                        else:
                            allow_print = False
                            break
            if allow_print == False:
                raise UserError('仕入先が複数にまたがるため出力できません。')
                
        return res
