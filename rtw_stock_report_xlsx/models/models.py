# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rtw_stock_report_xlsx(models.Model):
#     _name = 'rtw_stock_report_xlsx.rtw_stock_report_xlsx'
#     _description = 'rtw_stock_report_xlsx.rtw_stock_report_xlsx'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
