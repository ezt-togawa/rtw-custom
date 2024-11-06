# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
class rtw_sale_order_line(models.Model):
    _inherit = "sale.order.line"
    price_unit = fields.Monetary('Unit Price', required=True, digits='Product Price')
 
