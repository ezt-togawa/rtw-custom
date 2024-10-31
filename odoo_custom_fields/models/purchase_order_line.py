# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order.line"

    price_unit = fields.Monetary('Unit Price', required=True, digits='Product Price')
   