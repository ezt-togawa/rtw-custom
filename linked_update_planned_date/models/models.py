# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rtw_stock_move_line(models.Model):
#     _name = 'rtw_stock_move_line.rtw_stock_move_line'
#     _description = 'rtw_stock_move_line.rtw_stock_move_line'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
