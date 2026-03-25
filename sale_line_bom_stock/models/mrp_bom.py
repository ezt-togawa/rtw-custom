# -*- coding: utf-8 -*-
from odoo import models, fields


class BomLineForecast(models.Model):
    _inherit = "mrp.bom.line"
    
    minimum_quantity = fields.Float(string='最低数量', digits=(16, 2))
    unit_quantity = fields.Selection(
        selection=[
            ('1', '1個'),
            ('2', '2個')
        ],
        string='単位個数',
        default='',
    )