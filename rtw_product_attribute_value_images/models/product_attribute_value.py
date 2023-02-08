from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "product.attribute.value"

    image = fields.Binary("image")
