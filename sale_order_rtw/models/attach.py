# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_rtw(models.Model):
    _name = "item.attach"
    _description = "attach"
    _order = "sequence, id"

    name = fields.Char("attach")
    product_id = fields.Many2one("product.product", "Product")
    attach_file = fields.Binary("attach")
    sequence = fields.Integer(default=10, index=True)
    sale_line_ids = fields.Many2many(
        "sale.order.line", string="sale Lines", ondelete="cascade"
    )