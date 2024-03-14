# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit ='stock.move.line'

    pallet_id = fields.Many2one('stock.move.pallet', 'パレット')



