# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import format_date
from babel.dates import format_date as babel_format_date

class rtw_mrp_production_add_sol_date(models.Model):
    _inherit = 'mrp.production'
    
    shiratani_date = fields.Date(string='白谷到着日', readonly=True)
    depo_date = fields.Date(string='デポ１到着日', compute='_compute_sol_date')
    depo_date_2 = fields.Date(string='デポ２到着日', compute='_compute_depo_date_2')
    preferred_delivery_date = fields.Date(string='配達希望日', compute='_compute_sol_date')
    estimated_shipping_date = fields.Date(string='発送予定日')
    itoshima_shipping_date = fields.Date(string="糸島出荷日", compute='_compute_itoshima_shipping_date', inverse="_inverse_itoshima_shipping_date")
    itoshima_shipping_date_edit = fields.Date()
    arrival_date_itoshima_stock_move = fields.Date()
    mrp_mo_date = fields.Char(compute="_compute_mrp_mo_date")
    is_active = fields.Boolean(string='Active',default=False)


    def _compute_depo_date_2(self):
        sale_order = self.env["sale.order"].search([("name", "=", self.sale_reference)],limit=1)
        if sale_order:
            self.depo_date_2 = sale_order.warehouse_arrive_date_2
        else:
            self.depo_date_2 = ""
    
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
    
    @api.model
    def create(self, vals):
        record = super(rtw_mrp_production_add_sol_date, self).create(vals)
        sale_id = record._get_so_from_mrp(record)
        if sale_id:
            sol = self.env['sale.order.line'].search(
                [('order_id', '=', sale_id.id), ('product_id', '=', record.product_id.id)],
                limit=1
            )
            if sol:
                record.shiratani_date = sol.shiratani_date
        return record

    def _compute_sol_date(self):
        for record in self:
            sale_id = self._get_so_from_mrp(record)
            if sale_id:
                sol = self.env['sale.order.line'].search([('order_id', '=', sale_id.id),('product_id', '=', record.product_id.id)],limit=1)
                if sol:
                    # record.shiratani_date = sol.shiratani_date
                    record.depo_date = sol.depo_date
                else:
                    # record.shiratani_date = ''
                    record.depo_date = ''
                record.preferred_delivery_date = sale_id.preferred_delivery_date
            else:
                # record.shiratani_date = ''
                record.depo_date = ''
                record.preferred_delivery_date = ''

    def _compute_itoshima_shipping_date(self):
        for mo in self:
            if mo.arrival_date_itoshima_stock_move != mo.itoshima_shipping_date_edit and mo.itoshima_shipping_date_edit != False and mo.is_active == True:
                mo.itoshima_shipping_date = mo.itoshima_shipping_date_edit
                break
            if mo.arrival_date_itoshima_stock_move:
                mo.itoshima_shipping_date = mo.arrival_date_itoshima_stock_move
                break
            scheduled_date = ''
            if mo.itoshima_shipping_date_edit:
                scheduled_date = mo.itoshima_shipping_date_edit 
            elif mo.sale_reference and not mo.is_child_mo:
                so = self.env["sale.order"].search([('name', '=', mo.sale_reference)], limit=1)
                warehouse = mo.picking_type_id.warehouse_id
                if warehouse and warehouse.name == "糸島工場":
                    if so:
                        if so.sipping_to == "direct":
                            scheduled_date = so.estimated_shipping_date or ''
                        else:
                            scheduled_date = so.shiratani_entry_date or ''
                else:
                    pickings = self.env["stock.picking"].search([('sale_id', '=', so.id), ('state', '!=', 'cancel')])
                    for sp in pickings:
                        if sp.scheduled_date:                            
                            if not scheduled_date or scheduled_date > sp.scheduled_date:
                                scheduled_date = sp.scheduled_date
                                
                child_list = self.env["mrp.production"].search([('origin', '=', mo.name)]) 
                if child_list:
                    for child in child_list:
                        child.itoshima_shipping_date = scheduled_date
                                
            mo.itoshima_shipping_date = scheduled_date  
            
    def _inverse_itoshima_shipping_date(self):
        for mo in self:
            mo.itoshima_shipping_date_edit = mo.itoshima_shipping_date 
            mo.is_active = True
    def _compute_mrp_mo_date(self):
        for record in self:
            if record.itoshima_shipping_date:
                date_to_format = fields.Date.from_string(record.itoshima_shipping_date)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mrp_mo_date = f"{formatted_date} [{day_of_week}]"
            else:
                record.mrp_mo_date = ''    
 