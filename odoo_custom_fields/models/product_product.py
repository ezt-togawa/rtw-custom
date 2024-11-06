# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product_product(models.Model):
    _inherit = "product.product"

    lst_price = fields.Monetary(
        'Public Price', 
        digits='Product Price',
        currency_field='currency_id',
    )
    standard_price = fields.Monetary(
        'Cost', 
        digits='Product Price',
        currency_field='currency_id',
    )
   