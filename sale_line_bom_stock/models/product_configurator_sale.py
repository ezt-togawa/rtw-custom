
from odoo import models

class ProductConfiguratorSale(models.TransientModel):
    _inherit = "product.configurator.sale"
    
    def _get_order_line_vals(self,product_id):
        res = super()._get_order_line_vals(product_id)
        product = self.env["product.product"].browse(product_id)
        res.update(
            {
                "bom_id": min(product.bom_ids.ids),
            }
        )
        
        return res
