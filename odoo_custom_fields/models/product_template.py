# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product_supplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    price = fields.Monetary(
        'Price', 
        required=True, 
        digits='Product Price',
        currency_field='currency_id',
    )
   