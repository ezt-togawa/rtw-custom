from odoo import models, fields, api

class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    call_rate = fields.Float('Call Rate')
    
    @api.onchange('discount')
    def change_discount(self):
        for line in self:
            if line.discount:
                line.call_rate = 100 - line.discount
                
    @api.onchange('call_rate')
    def change_call_rate(self):
        for line in self:
            if line.call_rate:
                line.discount = 100 - line.call_rate
                
    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        super(SaleOrderLineExtend, self)._onchange_discount()

        if self.discount is not None:
            self.call_rate = 100 - self.discount
            