# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class rtw_sf(models.Model):
#     _name = 'rtw_sf.rtw_sf'
#     _description = 'rtw_sf.rtw_sf'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
a = fields.Selection([
        ('h', '高'),
        ('m', '中'),
        ('l', '低'),
        ], default='',
        string="" )