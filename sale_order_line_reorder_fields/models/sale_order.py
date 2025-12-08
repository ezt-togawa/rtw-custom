from odoo import models, fields, api

class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'
    
    def update_prices(self):
        for line in self.order_line:
            categ_name = line.product_id.categ_id.name if line.product_id and line.product_id.categ_id else False
            if categ_name == "汎用商品" and line.sale_order_sell_unit_price:
                line.write({
                    'preserved_price_value': line.sale_order_sell_unit_price,
                    'preserve_sell_unit_price': True
                })
        
        res = super(SaleOrderExtend, self.with_context(from_update_prices=True)).update_prices()
        percent_value = 0
        
        if self.pricelist_id and self.pricelist_id.discount_policy == 'without_discount' and self.pricelist_id.item_ids:
            price_item = self.pricelist_id.item_ids[0]
            
            if price_item.percent_price:
                percent_value = price_item.percent_price
            
        if percent_value and self.order_line:
            for line in self.order_line.with_context(from_update_prices=True):
                line.write({
                    'discount': percent_value,
                    'call_rate': 100 - percent_value
                })
            
        return res   