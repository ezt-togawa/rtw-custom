# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_custom_date(models.Model):
    _inherit = "sale.order.line"

    depo_date = fields.Date("Depo Date", tracking=True)
    shiratani_date = fields.Date("Shiratani Date", tracking=True)
    p_type = fields.Selection([
        ('special', '特注'),
        ('custom', '別注'),
    ],string = "製品タイプ")
#     _description = 'sale_order_line_custom_date.sale_order_line_custom_date'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
