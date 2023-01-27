# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_seal_of_approval(models.Model):
    _inherit = "sale.order"
#     _description = 'rtw_seal_of_approval.rtw_seal_of_approval'

    seal_of_approval = fields.Boolean("seal of approval")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
