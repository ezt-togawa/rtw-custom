# -*- coding: utf-8 -*-

from odoo import api,fields,models,_

class StockMoveLine(models.Model):
    _inherit ='stock.move.line'
   
    split = fields.Boolean(string='Split')



