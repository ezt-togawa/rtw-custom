# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveContainer(models.Model):
    _name = 'stock.move.container'
    _description = 'stock.move.container'

    @api.model
    def create(self, vals):
        result = super(StockMoveContainer, self).create(vals)
        return result

    name = fields.Char('Name', required=True)
    pallet_ids = fields.One2many(
        comodel_name="stock.move.pallet",
        inverse_name="container_id",
        string="PalletId", )
    # picking_ids = fields.One2many("stock.picking", compute='_compute_picking_ids', string="PickingId")
    #
    # @api.depends('move_line_ids')
    # def _compute_picking_ids(self):
    #     for line in self:
    #         line.picking_ids = line.move_line_ids.mapped('picking_id')
