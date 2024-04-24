# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_add_sol_date(models.Model):
    _inherit = 'mrp.production'
    
    shiratani_date = fields.Date(string='白谷到着日',compute='_compute_sol_date')
    depo_date = fields.Date(string='デポ到着日',compute='_compute_sol_date')
    preferred_delivery_date = fields.Date(string='配達希望日',compute='_compute_sol_date')

    def _compute_sol_date(self):
        sale_id = self.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
        if not sale_id and self.sale_reference:
            sale_id = self.env['sale.order'].search([('name','=',self.sale_reference)])
        if sale_id:
            sol = self.env['sale.order.line'].search([('order_id', '=', sale_id.id),('product_id', '=', self.product_id.id)],limit=1)
            if sol:
                self.shiratani_date = sol.shiratani_date
                self.depo_date = sol.depo_date
            else:
                self.shiratani_date = ''
                self.depo_date = ''
                
            self.preferred_delivery_date = sale_id.preferred_delivery_date
        else:
            self.shiratani_date = ''
            self.depo_date = ''
            self.preferred_delivery_date = ''