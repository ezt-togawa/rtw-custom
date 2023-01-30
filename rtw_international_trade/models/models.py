# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_international_trade(models.Model):
    _name = 'rtw_international_trade.rtw_international_trade'
#     _description = 'rtw_international_trade.rtw_international_trade'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
