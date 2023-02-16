# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMovePallet(models.Model):
    _inherit ='stock.move.pallet'
   
    container_id = fields.Many2one('stock.move.container', 'ContainerId')



