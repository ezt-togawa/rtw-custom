# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMovePallet(models.Model):
    _name = 'stock.move.pallet'
    _description = 'stock.move.pallet'

    @api.model
    def create(self, vals):
        result = super(StockMovePallet, self).create(vals)
        return result

    name = fields.Char('Name', required=True, translate=True)
    move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="pallet_id",
        string="MoveLineId", )
    picking_ids = fields.One2many(
        "stock.picking", compute='_compute_picking_ids', string="PickingId", store=False)

    @api.depends('move_line_ids')
    def _compute_picking_ids(self):
        for line in self:
            line.picking_ids = line.move_line_ids.mapped('picking_id')

class StockPickingPallet(models.Model):
    _inherit = 'stock.picking'

    pallet_id = fields.Many2one(
        'stock.move.pallet',
        string='パレット',
        compute='_compute_pallet_id',
    )

    @api.depends('move_line_ids')
    def _compute_pallet_id(self):
        for picking in self:
            pallet_ids = picking.move_line_ids.mapped('pallet_id')
            if pallet_ids:
                picking.pallet_id = pallet_ids[0]
            else:
                picking.pallet_id = False
