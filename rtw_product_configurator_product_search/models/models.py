# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rtw_product_configurator_ctm(models.Model):
#     _name = 'rtw_product_configurator_ctm.rtw_product_configurator_ctm'
#     _description = 'rtw_product_configurator_ctm.rtw_product_configurator_ctm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
