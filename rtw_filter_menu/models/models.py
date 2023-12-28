# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class rtw_filter_menu(models.Model):
#     _name = 'rtw_filter_menu.rtw_filter_menu'
#     _description = 'rtw_filter_menu.rtw_filter_menu'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class IrFiltersCus(models.Model):
    _inherit = 'ir.filters'
    
    name = fields.Char(string='Filter Name', translate=False, required=True)