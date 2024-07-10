from odoo import models, fields, api

class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'
    
    def update_prices(self):
        res = super(SaleOrderExtend,self).update_prices()
        percent_value = 0
        
        if self.pricelist_id and self.pricelist_id.discount_policy == 'without_discount' and self.pricelist_id.item_ids:
            price_item = self.pricelist_id.item_ids[0]
            
            if price_item.percent_price:
                percent_value = price_item.percent_price
            
        if percent_value and self.order_line:
            for line in self.order_line:
                line.discount = percent_value
                line.call_rate = 100 - line.discount
            
        return res   