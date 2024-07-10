# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_add_sol_date(models.Model):
    _inherit = 'mrp.production'
    
    shiratani_date = fields.Date(string='白谷到着日', compute='_compute_sol_date')
    depo_date = fields.Date(string='デポ到着日', compute='_compute_sol_date')
    preferred_delivery_date = fields.Date(string='配達希望日', compute='_compute_sol_date')
    estimated_shipping_date = fields.Date(string='発送予定日')
    itoshima_shipping_date = fields.Date(string="糸島出荷日", compute='_compute_itoshima_shipping_date')

    def _get_so_from_mrp(self , mrp_production , count = 0):
          if count >= 10:
              return False
          if not mrp_production.origin:
              return False
          
          sale_order_id = False
          if '/MO/' in mrp_production.origin:
              mrp = self.env['mrp.production'].search([('name','=',mrp_production.origin)])
              if mrp:
                  count += 1
                  sale_order_id = self._get_so_from_mrp(mrp, count)
          else:
              sale_order_id = self.env['sale.order'].search([('name','=',mrp_production.origin)])
          return sale_order_id
    
    def _compute_sol_date(self):
        for record in self:
            sale_id = self._get_so_from_mrp(record)
            if sale_id:
                sol = self.env['sale.order.line'].search([('order_id', '=', sale_id.id),('product_id', '=', record.product_id.id)],limit=1)
                if sol:
                    record.shiratani_date = sol.shiratani_date
                    record.depo_date = sol.depo_date
                else:
                    record.shiratani_date = ''
                    record.depo_date = ''
                record.preferred_delivery_date = sale_id.preferred_delivery_date
            else:
                record.shiratani_date = ''
                record.depo_date = ''
                record.preferred_delivery_date = ''
    
    def _compute_itoshima_shipping_date(self):
        for mo in self:
            scheduled_date = ''
            if mo.sale_reference:
                so = self.env["sale.order"].search([('name', '=', mo.sale_reference)], limit=1)
                if so:
                    pickings = self.env["stock.picking"].search([('sale_id', '=', so.id)])
                    for sp in pickings:
                        if sp.scheduled_date:                            
                            if not scheduled_date or scheduled_date > sp.scheduled_date:
                                scheduled_date = sp.scheduled_date
                                
            mo.itoshima_shipping_date = scheduled_date          
                