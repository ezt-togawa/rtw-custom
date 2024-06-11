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
    move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="pallet_id",
        string="MoveId", )
    picking_ids = fields.One2many(
        "stock.picking", compute='_compute_picking_ids', string="PickingId", store=False)

    @api.depends('move_ids')
    def _compute_picking_ids(self):
        for line in self:
            line.picking_ids = line.move_ids.mapped('picking_id')

class StockPickingPallet(models.Model):
    _inherit = 'stock.picking'
    pallet_ids = fields.Char(
        string='パレット',
        compute='_compute_pallet_ids',
        store=True
    )

    @api.depends('move_ids_without_package','move_ids_without_package.pallet_id','move_ids_without_package.pallet_id.name')
    def _compute_pallet_ids(self):
        for picking in self:
            pallet_ids = picking.move_ids_without_package.mapped('pallet_id').mapped('name')
            if pallet_ids:
                picking.pallet_ids = ','.join(pallet_ids)
            else:
                picking.pallet_ids = ''
