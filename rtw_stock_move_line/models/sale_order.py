# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_rtw_stock_move_line(models.Model):
    _inherit = "sale.order"
    delivery_confirmation = fields.Boolean('delivery_confirmation', default=0)

