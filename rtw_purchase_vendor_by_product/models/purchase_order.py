# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    order_line_exists = fields.Boolean(
        string='Order Line Exists',
        compute='_compute_order_line_exists',
        store=True
    )
    partner_id = fields.Many2one('res.partner',  domain="[('id', 'in', partner_ids)]")
    partner_ids = fields.Many2many('res.partner',compute ='compute_partner_ids')

    def compute_partner_ids(self):
        partner_ids = []
        for line in self:
            if line.order_line:
                for order in line.order_line:
                    partner_ids.extend(order.product_id.seller_ids.mapped('name.id'))
                line.partner_ids =tuple(partner_ids)
            else:
                partner_ids = self.env['res.partner'].search([]).ids
                line.partner_ids = partner_ids
      
    @api.depends('order_line')
    def _compute_order_line_exists(self):
        for order in self: 
            order.order_line_exists = bool(order.order_line)

    @api.onchange('order_line')
    def onchange_order_line(self):
        supplier_id = False
        partner_ids = []
        for line in self:
            if line.order_line:
                for order in line.order_line:
                    partner_ids = order.product_id.seller_ids.mapped('name.id')
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
            return {'domain': {'partner_id': [('id', 'in', partner_ids), '|', ('company_id', '=', False), ('company_id', '=', line.company_id.id)]}}
        else:
            return {'domain': {'partner_id': ['|', ('company_id', '=', False), ('company_id', '=', line.company_id.id)]}}

    @api.onchange('currency_id','partner_id')
    def onchange_currency_id(self):
        if self.order_line:
            if self.partner_id:
               for line in self.order_line:
                   line._onchange_quantity()