from odoo import models

class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'

    def update_prices(self):
        price_unit_values = {}
        for line in self.order_line:
            if line.product_id and line.product_id.categ_id and line.product_id.categ_id.name == '汎用商品':
                price_unit_values[line.id] = line.price_unit
        
        res = super(SaleOrderExtend,self).update_prices()
        
        for line in self.order_line:
            if line.id in price_unit_values:
                line.price_unit = price_unit_values[line.id]
        
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