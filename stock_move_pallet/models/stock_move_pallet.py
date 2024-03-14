# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMovePallet(models.Model):
    _name = 'stock.move.pallet'
    _description = 'stock.move.pallet'

    @api.model
    def create(self, vals):
        result = super(StockMovePallet, self).create(vals)
        return result

    name = fields.Char('Name', required=True , translate=True)
    move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="pallet_id",
        string="MoveLineId", )
    picking_ids = fields.One2many("stock.picking", compute='_compute_picking_ids', string="PickingId")

    @api.depends('move_line_ids')
    def _compute_picking_ids(self):
        for line in self:
            line.picking_ids = line.move_line_ids.mapped('picking_id')
