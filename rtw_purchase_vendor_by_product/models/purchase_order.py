# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    order_line_exists = fields.Boolean(
        string='Order Line Exists',
        compute='_compute_order_line_exists',
        store=True
    ) 
    @api.depends('order_line')
    def _compute_order_line_exists(self):
        for order in self: 
            order.order_line_exists = bool(order.order_line)

    @api.onchange('order_line')
    def onchange_order_line(self):
        supplier_id = False
        for line in self:
            if line.order_line:
                for order in line.order_line:
                    if order.product_id.seller_ids:
                        if not supplier_id:
                            supplier_id = order.product_id.seller_ids[0].name.id
        if self.order_line:
            if not supplier_id:
                return {'domain': {'partner_id': ['|', ('company_id', '=', False), ('company_id', '=', line.company_id.id)]}}
            if not self.partner_id:
                self.partner_id = supplier_id
                self.currency_id = self.partner_id.property_purchase_currency_id.id
                
                if self.partner_id and self.currency_id:
                    for line in self.order_line:
                        line.onchange_product_id()
            # return {'domain': {'partner_id': [('id', '=', self.partner_id.id), '|', ('company_id', '=', False), ('company_id', '=', line.company_id.id)]}}
        else:
            return {'domain': {'partner_id': ['|', ('company_id', '=', False), ('company_id', '=', line.company_id.id)]}}

    @api.onchange('currency_id','partner_id')
    def onchange_currency_id(self):
        if self.order_line:
            if self.partner_id:
               for line in self.order_line:
                   line._onchange_quantity()