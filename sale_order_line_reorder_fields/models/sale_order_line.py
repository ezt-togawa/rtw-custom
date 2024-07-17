from odoo import models, fields, api

class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    call_rate = fields.Float('Call Rate')
    updating_discount  = fields.Boolean()
    updating_call_rate  = fields.Boolean()
    
    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self:
            if line.discount:
                line.call_rate = 100 - line.discount
                line.updating_discount = True

    @api.onchange('call_rate')
    def _onchange_call_rate(self):
        for line in self:
            if line.call_rate:
                line.discount = 100 - line.call_rate
                line.updating_call_rate = True
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.ensure_one()
        if self.updating_discount or self.updating_call_rate:
            return
        elif self.order_id and self.order_id.pricelist_id and self.order_id.pricelist_id.discount_policy == 'without_discount' and self.order_id.pricelist_id.item_ids:
            price_item = self.order_id.pricelist_id.item_ids[0]
            if price_item.percent_price:
                percent_value = price_item.percent_price
                self.discount = percent_value
                self.call_rate = 100 - self.discount
        
    def write(self, vals):
        res = super(SaleOrderLineExtend, self).write(vals)
        for line in self:
            if line.call_rate and line.discount:
                break
            elif line.discount:
                line.call_rate = 100 - line.discount
        return res
