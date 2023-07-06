# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_shipping_type(models.Model):
    _inherit = "sale.order"

    shipping_type = fields.Selection([('air', '空路'), ('sea', '海路')], '海外', default=None)

class stock_picking_shipping_type(models.Model):
    _inherit = "stock.picking"

    shipping_type = fields.Char('海外' , compute="_compute_shipping_type")
    overseas = fields.Boolean('Overseas' , compute="_compute_overseas")

    def _compute_shipping_type(self):
        sale_order = self.sale_id
        if sale_order:
            if sale_order.shipping_type == 'air':
                self.shipping_type = '空路'
            elif sale_order.shipping_type == 'sea':
                self.shipping_type = '海路'
            else:
                self.shipping_type = ''
        else:
            self.shipping_type = ''

    def _compute_overseas(self):
        sale_order = self.sale_id
        if sale_order:
            if sale_order.overseas:
                self.overseas = True
            else:
                self.overseas = False
        else:
            self.overseas = False
