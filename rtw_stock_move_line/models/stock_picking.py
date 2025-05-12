# -*- coding: utf-8 -*-

from odoo import fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    primary_shipment = fields.Boolean('一次出荷', default=False)  

    def toggle_primary_shipment(self):
        for record in self:
            record.primary_shipment = not record.primary_shipment 


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        if self._name == 'purchase.order':
            stock_picking = self.env['stock.picking'].search([('origin', '=', self.name)])
            if stock_picking:
                for stock in stock_picking:
                    for move in stock.move_ids_without_package:
                        purchase_order_line = self.env['purchase.order.line'].search([('product_id','=',move.product_id.id),('order_id','=',move.origin)],limit=1)
                        move.write({'description_picking': purchase_order_line.name})
        return result