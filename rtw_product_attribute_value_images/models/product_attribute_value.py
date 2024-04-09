from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "product.attribute.value"

    image = fields.Binary("image")
    child_attribute_ids = fields.Many2many(
        'product.attribute.value',
        'product_attribute_value_related_rel',
        'value_id',
        'related_value_id',
        string='Related Attribute Values',
        domain=lambda self: "[('id','!=',id)]",
    )

