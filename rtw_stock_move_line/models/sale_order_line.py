# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_rtw_stock_move_line(models.Model):
    
    _inherit = "sale.order.line"

    remarks = fields.Char('remarks')
