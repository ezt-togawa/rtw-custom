# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMovePallet(models.Model):
    _inherit ='stock.move.pallet'
   
    container_id = fields.Many2one('stock.move.container', 'ContainerId')

    status = fields.Char('ステータス', compute="_compute_status", store=True,default="配送待")

    @api.depends('move_ids.state')
    def _compute_status(self):
        for record in self:
            if all(line.state == 'done' for line in record.move_ids):
                status = "配送完了"
            else:
                status = "配送待"  
            record.status = status


