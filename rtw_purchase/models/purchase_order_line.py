# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order.line"

    sale_order_ids = fields.Char("sale order", compute='_compute_sale_order')
    sale_order_names = fields.Char("sale order title", compute='_compute_sale_order')

    @api.depends('move_dest_ids.group_id.mrp_production_ids')
    def _compute_sale_order(self):
        for purchase in self:
            purchase.sale_order_ids = False
            move_dest_ids = purchase.move_dest_ids.group_id.mrp_production_ids | purchase.move_ids.move_dest_ids.group_id.mrp_production_ids
            move_ids = purchase.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                order = []
                name = []
                for rec in move_dest_ids:
                    if rec.origin:
                        order.append(rec.origin)
                    if self.env['sale.order'].search([('name', '=', rec.origin)]).title:
                        name.append(self.env['sale.order'].search([('name', '=', rec.origin)]).title)
                purchase.sale_order_ids = ','.join(order)
                purchase.sale_order_names = ','.join(name)
            else:
                purchase.sale_order_ids = False
                purchase.sale_order_names = False
