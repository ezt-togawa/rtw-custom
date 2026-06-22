# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMovePallet(models.Model):
    _inherit ='stock.move.pallet'
   
    container_id = fields.Many2one('stock.move.container', 'ContainerId')

    status = fields.Char('ステータス', compute="_compute_status", store=True, default="配送待")

    @api.depends('move_ids.state', 'move_ids.picking_id')
    def _compute_status(self):
        for record in self:
            # 運送(Piking)に紐づく配送(move)のみ対象にしてステータスチェックをする
            picking_moves = record.move_ids.filtered(lambda m: m.picking_id)

            if picking_moves and all(line.state == 'done' for line in picking_moves):
                status = "配送完了"
            else:
                status = "配送待"  
            record.status = status


